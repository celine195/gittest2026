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
    # 💡 確保不論是 POST 還是 GET，一進來都先把 form 建立好，徹底解決 UnboundLocalError！
    form = ReservationForm()
    
    if request.method == "POST":
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. 建立預約物件，但先不要寫入資料庫 (commit=False)
                    reservation = form.save(commit=False)
                    
                    # 💡 2. 核心修正：直接去拿網頁上打的老師名字文字，塞進 user 欄位
                    # ❌ 絕對不要寫成 reservation.user = request.user 喔！
                    reservation.user = request.POST.get('user')
                    reservation.exclude_weeks = request.POST.get('exclude_weeks', '')
                    # 3. 正式存檔（這樣 Django 就會自動把日期、裝置、名字全部一起存進去！）
                    reservation.save()
                    messages.success(request, "🎉 您的借用申請已成功送出！請等待管理員審核。")
                    return redirect('allreservation_view')
            except Exception as e:
                print("❌ 存檔時發生資料庫錯誤：", e)
        else:
            print("❌ 表單驗證失敗！詳細原因：", form.errors)
            
    # 💡 這裡統一交給同一個 Form 元件去渲染畫面
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
        
        # 抓出這筆申請資料
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
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)
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
    next_url = request.GET.get('next') or request.POST.get('next')
    logout(request)
    if next_url:
        return redirect(next_url)
    else:
        return redirect('login')
    


def all_reservation_list(request):
    borrow_records = Borrowlist.objects.all().order_by('-id')
    return render(request, 'all_reservation.html', {
        'borrow_records': borrow_records
    })
