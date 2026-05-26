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
                    
                    # 3. 正式存檔（這樣 Django 就會自動把日期、裝置、名字全部一起存進去！）
                    reservation.save()
                    return redirect('/reservations/')
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

    today_records = reservationlist.objects.filter(date=today).order_by('time_id')
    

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

class AllreservationView(ListView):
    model = Borrowlist
    template_name = 'all_reservation.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_str = self.request.GET.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                target_date = date.today()
        else:
            target_date = date.today()

        periods = ['1', '2', '3', '4', '4.5', '5', '6', '7', '8']
        
        period_names = {
            '1': '第一節', '2': '第二節', '3': '第三節', '4': '第四節',
            '4.5': '午休', '5': '第五節', '6': '第六節', '7': '第七節', '8': '第八節'
        }
        all_cars = devicecar.objects.all()
        day_schedules = reservationlist.objects.filter(date=target_date)
        table_data = {p: {} for p in periods}
        
        for sch in day_schedules:
            try:
                
                original_form = Borrowlist.objects.get(id=sch.list_id)
                teacher = CustomRegistrationForm.objects.get(id=original_form.user.id)
                table_data[str(sch.time_id)][sch.devicecar_id] = {
                    'form': original_form,
                    'teacher': teacher
                }
            except (Borrowlist.DoesNotExist, CustomRegistrationForm.DoesNotExist):
                continue

        context['target_date'] = target_date
        context['periods'] = periods
        context['period_names'] = period_names
        context['all_cars'] = all_cars
        context['table_data'] = table_data
        
        return context
