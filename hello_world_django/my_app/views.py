from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseNotAllowed,
)
from my_app.db_interface import MySqlInterface
from uuid import uuid4
from util.check_input import *
from django.utils.functional import classproperty
from django.utils.decorators import classonlymethod
from asgiref.sync import iscoroutinefunction, markcoroutinefunction

import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"><body>It is now %s.</body></html>' % now
    return HttpResponse(html)

def index(request):
    return HttpResponse("Hello, world!")

class View:
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """

    http_method_names = [
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classproperty
    def view_is_async(cls):
        handlers = [
            getattr(cls, method)
            for method in cls.http_method_names
            if (method != "options" and hasattr(cls, method))
        ]
        if not handlers:
            return False
        is_async = iscoroutinefunction(handlers[0])
        if not all(iscoroutinefunction(h) == is_async for h in handlers[1:]):
            raise ImproperlyConfigured(
                f"{cls.__qualname__} HTTP handlers must either be all sync or all "
                "async."
            )
        return is_async

    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(
                    "The method name %s is not accepted as a keyword argument "
                    "to %s()." % (key, cls.__name__)
                )
            if not hasattr(cls, key):
                raise TypeError(
                    "%s() received an invalid keyword %r. as_view "
                    "only accepts arguments that are already "
                    "attributes of the class." % (cls.__name__, key)
                )

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            self.setup(request, *args, **kwargs)
            if not hasattr(self, "request"):
                raise AttributeError(
                    "%s instance has no 'request' attribute. Did you override "
                    "setup() and forget to call super()?" % cls.__name__
                )
            return self.dispatch(request, *args, **kwargs)

        view.view_class = cls
        view.view_initkwargs = initkwargs

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__annotations__ = cls.dispatch.__annotations__
        # Copy possible attributes set by decorators, e.g. @csrf_exempt, from
        # the dispatch method.
        view.__dict__.update(cls.dispatch.__dict__)

        # Mark the callback if the view class is async.
        if cls.view_is_async:
            markcoroutinefunction(view)

        return view

    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, "get") and not hasattr(self, "head"):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning(
            "Method Not Allowed (%s): %s",
            request.method,
            request.path,
            extra={"status_code": 405, "request": request},
        )
        response = HttpResponseNotAllowed(self._allowed_methods())

        if self.view_is_async:

            async def func():
                return response

            return func()
        else:
            return response

    def options(self, request, *args, **kwargs):
        """Handle responding to requests for the OPTIONS HTTP verb."""
        response = HttpResponse()
        response.headers["Allow"] = ", ".join(self._allowed_methods())
        response.headers["Content-Length"] = "0"

        if self.view_is_async:

            async def func():
                return response

            return func()
        else:
            return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

class TravelRequestView(View):
    def post(self, request):
        """
        Manages travel requests submissions form by saving the request and identifying the sender email.
        
        Args:
            request: the client side request (in this version, it comes from webflow)
        
        Returns:
            TODO
        """
      
        db = MySqlInterface()
        
        try:
            checker = check_input_factory(CheckTravelRequestFields.TYPE, db=db)
            checker.check(request.POST)
            
            # if user is not verified yet
            email = request.POST.get('user_email') + '@' + request.POST.get('uni_domains')
            user, created = db.upsert_user_by_mail(email)

            travel_request = db.insert_travel_request(
                user_email = user.email, 
                user_uuid = user.uuid, 
                arrival_country  = request.POST.get('arrival_country'),
                departure_country = request.POST.get('departure_country'),
                travel_period = request.POST.get('travel_period'),
                travel_requests = request.POST.get('travel_requests'),
                token = uuid4()
            )

            verification_link = os.path.join("https://", HOSTNAME, VerifyEmailView.URL, travel_request.token)
            template_info = {
                'type': EmailTemplateManagerConstant.TRAVEL_REQUEST_VERIFICATION.value,
                'user_name': request.POST.get('user_name'),
                'verification_link': verification_link
            }

            email_manager = email_template_manager_factory(template_info)
            email_content = email_manager.fill()
            # send verification email
            # TODO sostituire make
            send_email(GO2RAIL_EMAIL, user.email, email_manager.EMAIL_SUB, email_content)
            return HttpResponse("successful_request")

        except Exception as e:
            log.exception(e)
            return HttpResponseBadRequest("Something went wrong. Check your input.")
        




