from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("date", views.current_datetime),
    path("travel-request-view", views.TravelRequestView)
]