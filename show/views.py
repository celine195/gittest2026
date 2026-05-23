from django.shortcuts import render , redirect , get_object_or_404
from .models import *  
from .models import Borrowlist, ReservationSchedule as ReservationList
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
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

def create_reservation(borrow_record):
    """
    自動化核心：當管理員按下核准，這個函式會被觸發。
    它會自動計算日期，並在 reservationlist 資料表裡面建立對應的排程紀錄。
    """
    try:
        # 1. 先幫老師自動分配一台載具車 (依據需求文件：根據條件種類分配)
        # 這裡先簡單撈出符合老師申請種類的第一台載具車，實務上可再寫複雜的庫存扣除邏輯
        # car = DeviceCar.objects.filter(device_type=borrow_record.device_type).first()
        # cart_id_to_assign = car if car else None
        cart_id_to_assign = None # 這裡先設 None，如果你還沒建立 DeviceCar 的資料

        # 2. 判斷是「單次借用」還是「每週借用」
        if borrow_record.usage_type == 'once':
            # 【單次借用】：只在 ReservationList 建立 1 筆紀錄
            ReservationList.objects.create(
                reservation_id=borrow_record, # 外鍵：對應這筆申請
                date=borrow_record.start_date, # 使用日期就是開始日期
                period=borrow_record.periods,  # 節次
                cart_id=cart_id_to_assign      # 分配的載具車
            )
            
        elif borrow_record.usage_type == 'weekly':
            # 【每週借用】：要從 start_date 一路跑到 end_date，每隔 7 天建立一筆
            current_date = borrow_record.start_date
            end_date = borrow_record.end_date
            
            # 解析排除週次（例如老師填 "8"，代表第 8 週不產生）
            # 為了防呆，先把老師填的字串轉成數字清單，若沒填就是空清單
            exclude_weeks_list = []
            if borrow_record.exclude_weeks:
                # 假設老師填 "8" 或 "8,9"，拆開並轉成數字
                exclude_weeks_list = [int(w.strip()) for w in borrow_record.exclude_weeks.split(',') if w.strip().isdigit()]

            week_counter = 1 # 用來計算目前是第幾週
            
            while current_date <= end_date:
                # 檢查這一週有沒有被列在「排除週次」裡面
                if week_counter not in exclude_weeks_list:
                    # 如果沒有被排除，就在預約總表建立紀錄！
                    ReservationList.objects.create(
                        reservation_id=borrow_record,
                        date=current_date,           # 自動計算出來的該週日期
                        period=borrow_record.periods, # 節次
                        cart_id=cart_id_to_assign
                    )
                
                # 日期往後推 7 天（下一週），週數 +1
                current_date += timedelta(days=7)
                week_counter += 1
                
        return True # 全部建立成功，回傳 True
    except Exception as e:
        print(f"自動產生預約失敗，原因: {e}")
        return False


def review_borrow(request, pk):
    """
    功能：處理管理員的審核動作（核准/不通過）
    pk: 代表那筆借用申請的 id
    """
    if request.method == 'POST':
        # 1. 撈出這筆申請單，撈不到就噴 404
        record = get_object_or_404(Borrowlist, id=pk)
        
        # 2. 獲取管理員按下的是哪個按鈕 ('approve' 或 'reject')
        action = request.POST.get('action')
        
        # 3. 使用 transaction 確保狀態修改與預約排程產生綁在同一個原子操作中
        with transaction.atomic():
            if action == 'approve':
                # 變更狀態為已核准
                record.status = '已核准'
                record.save()
                
                # 【核心自動化】狀態變更後，觸發你原本寫好的預約排程小幫手！
                # 它會根據這筆 record 的日期、節次，自動去 ReservationList 畫格子
                success = reservation_create(record) 
                
                if success:
                    messages.success(request, f"申請單 #{pk} 已核准，系統已自動產生預約排程！")
                else:
                    # 萬一設備不夠導致預約失敗，讓資料庫回滾，狀態改回待審核
                    raise transaction.TransactionManagementError("設備不足，無法核准")
                    
            elif action == 'reject':
                record.status = '不通過'
                record.save()
                messages.warning(request, f"申請單 #{pk} 已被拒絕。")
                
        return redirect('view_borrow_list') # 處理完後，跳轉回初核列表頁

class AllreservationView(ListView):
    model = list
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
                
                original_form = list.objects.get(id=sch.list_id)
                teacher = user.objects.get(id=original_form.user_id)
                table_data[str(sch.time_id)][sch.devicecar_id] = {
                    'form': original_form,
                    'teacher': teacher
                }
            except (list.DoesNotExist, user.DoesNotExist):
                continue

        context['target_date'] = target_date
        context['periods'] = periods
        context['period_names'] = period_names
        context['all_cars'] = all_cars
        context['table_data'] = table_data
        
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
