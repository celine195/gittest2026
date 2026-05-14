from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.reservation_create, name='reservation_create'),
]