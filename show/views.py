from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import ReservationForm

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