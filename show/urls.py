from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('allreservation/', views.all_reservation_list, name= 'allreservation_view'),
]