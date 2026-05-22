from django.shortcuts import render, redirect
from .models import *  
from .models import Borrowlist, ReservationSchedule  
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from .form import ReservationForm, DeviceForm, TimeForm


def reservation_create(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        device_form = DeviceForm(request.POST)
        time_form = TimeForm(request.POST)
        
        if form.is_valid() and device_form.is_valid() and time_form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user 
            reservation.save()  
            
            device_form.save()  
            time_form.save()
            return redirect('success')  
    else:
        form = ReservationForm()
        device_form = DeviceForm()
        time_form = TimeForm()

    return render(request, 'forms.html', {
        'form': form,
        'device_form': device_form,
        'time_form': time_form

    })


def view_borrow_list(request):
    """
    頁面：管理員初核頁面
    功能：查看所有教師送出的借用申請資料
    """
    borrow_records = Borrowlist.objects.all().order_by('-id')
    
    return render(request, 'borrow_list.html', {
        'borrow_records': borrow_records
    })


def today_reservation_list(request):

    today = timezone.localdate()

    today_records = ReservationSchedule.objects.filter(date=today).order_by('period')
    

    return render(request, 'today_reservation.html', {
        'today_records': today_records,
        'today': today
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                

                if hasattr(user, 'role') and user.role == 'admin':
                    return redirect('today_reservation')  
                else:
                    return redirect('view_borrow_list')  
            else:
                messages.error(request, "帳號或密碼錯誤")
        else:
            messages.error(request, "請輸入正確的帳號密碼")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  
