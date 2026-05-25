from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('allreservation/', AllreservationView.as_view(), name= 'allreservation_view'),
]