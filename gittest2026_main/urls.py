"""
URL configuration for gittest2026_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import *
from show import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path("",include("show.urls")),
    path('reservations/', views.reservation_create,name='submit_borrow'),
    path('borrow/', views.view_borrow_list, name='view_borrow_list'),
    path('today/', views.today_reservation_list, name='today_reservation'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.all_reservation_list, name= 'allreservation_view'),
]

