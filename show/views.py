from django.shortcuts import render
from .models import *  
from .models import list
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    # 根據需求文件，由近到遠撈出所有申請，並預先載入對應的教師(user)資料以利效能優化
    borrow_records = BorrowList.objects.all().select_related('user').order_by('-id')
    
    return render(request, 'borrow_list.html', {
        'borrow_records': borrow_records
    })