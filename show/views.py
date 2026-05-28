from django.shortcuts import render , redirect , get_object_or_404
from .models import *  
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .form import ReservationForm
from datetime import date, datetime
from django.views.generic import ListView
from django.http import HttpResponseRedirect

def reservation_create(request):
    form = ReservationForm()
    
    if request.method == "POST":
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():

                    reservation = form.save(commit=False)
                    

                    reservation.user = request.POST.get('user')
                    
                    reservation.save()
                    return redirect('/reservations/')
            except Exception as e:
                print("存檔時發生資料庫錯誤：", e)
        else:
            print("表單驗證失敗！詳細原因：", form.errors)
            
    device_form = form
    time_form = form

    return render(request, 'forms.html', {
        'form': form,
        'device_form': device_form,
        'time_form': time_form,
    })

def view_borrow_list(request):
    """
    頁面：管理員初核頁面
    功能：查看所有教師送出的借用申請資料
    """
    if request.method == "POST":
        record_id = request.POST.get('record_id')
        action = request.POST.get('action')

        record = get_object_or_404(Borrowlist, id=record_id)
        
        if action == 'approve':
            record.status = '已核准'
            record.save()
            messages.success(request, f"已成功核准 #{record.id} 的借用申請！")
        elif action == 'reject':
            record.status = '已拒絕'
            record.save()
            messages.warning(request, f"已拒絕 #{record.id} 的借用申請。")
            
        # 處理完後，重新導向回自己，刷新頁面狀態
        return HttpResponseRedirect('/borrow/')

    # 平常管理員直接進網頁時（GET 請求），只負責顯示名單
    borrow_records = Borrowlist.objects.all().order_by('-id')
    return render(request, 'borrow_list.html', {
        'borrow_records': borrow_records
    })


def today_reservation_list(request):

    today = timezone.localdate()

    today_records = Borrowlist.objects.filter(start_date=today).order_by('time_id')
    

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


def all_reservation_list(request):
    borrow_records = Borrowlist.objects.all().order_by('-id')
    return render(request, 'all_reservation.html', {
        'borrow_records': borrow_records
    })
