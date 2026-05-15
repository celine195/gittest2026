from django.shortcuts import render
from models import *
from django.shortcuts import render, redirect
#from .forms import ReservationForm

class ReservationForm(forms.ModelForm):
    class Meta:
        model = list
        fields = [
            'user_id',
            'phone',
            'usage_type',
            'time_id',
            'periods',
            'classroom',
            'device_id',
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

    return render(request, 'templates/form.html', {'form': form})