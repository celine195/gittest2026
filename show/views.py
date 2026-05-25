from django.shortcuts import render , redirect , get_object_or_404
from .models import *  
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .form import ReservationForm, DeviceForm, TimeForm
from datetime import date, datetime
from django.views.generic import ListView

def reservation_create(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        device_form = DeviceForm(request.POST)
        time_form = TimeForm(request.POST)
        
        if form.is_valid() and device_form.is_valid() and time_form.is_valid():
            with transaction.atomic():
                t_obj = time_form.save()
                d_obj, created = device.objects.get_or_create(device_type=device_form.cleaned_data['device_type'])
    
                reservation = form.save(commit=False)
                reservation.user = request.user 
                reservation.time = t_obj  # 綁定時間外鍵
                reservation.device = d_obj  # 綁定載具外鍵
                reservation.save()
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
        return redirect('view_borrow_list')

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
