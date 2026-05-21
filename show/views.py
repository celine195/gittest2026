from django.shortcuts import render , redirect
from .models import *  
from .models import Borrowlist
from django.contrib.auth.decorators import login_required
from django import forms

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Borrowlist
        fields = [
            'user_id',
            'phone',
            #'usage_type_choices',
            'usage_type',
            'device_id',
            'time_id',
            'device_amount',
        ]

def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user  # 自動帶入登入者
            reservation.save()
            return redirect('success')
    else:
        form = ReservationForm()

    return render(request, 'forms.html', {'form': form})


def view_borrow_list(request):
    """
    頁面：管理員初核頁面
    功能：查看所有教師送出的借用申請資料
    """
    # 根據需求文件，由近到遠撈出所有申請，並預先載入對應的教師(user)資料以利效能優化
    borrow_records = Borrowlist.objects.all().order_by('-id')
    
    return render(request, 'borrow_list.html', {
        'borrow_records': borrow_records
    })