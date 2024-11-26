"""
URL configuration for hello_world_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # configured the url
    path('my_app/', include("my_app.urls")),
    path("", views.index, name="index"),
    path("travel/request", views.TravelRequestView.as_view(), name="travel_request"),
    # path("memorandum/request", views.MemorandumRequestView.as_view(), name="memorandum_request"),
    # path("memorandum/confirm", views.MemorandumConfirmationView.as_view(), name="memorandum_request"),
    # path("email/verify", views.VerifyEmailView.as_view(), name="verify_email"),
    # path("bot/otp/generate", views.BotOtpGenerationView.as_view(), name="generate_otp"),
    # path("bot/otp/verify", views.BotOtpVerificationView.as_view(), name="verify_otp"),
    # path("bot/user/confirmed", views.BotCheckUserConfirmedView.as_view(), name="check_confirmed_user"),
    # path("travel/create", views.CreateTravelView.as_view(), name="create_travel"),
    # path("group/create", views.CreateTravelGroupView.as_view(), name="create_group"),
]
