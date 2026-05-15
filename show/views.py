from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import ReservationList
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




def create_reservation(borrow):

    time_slot = borrow.time_slot

    start_date = time_slot.start_date

    device = borrow.device

    amount = borrow.device_amount

    for period in time_slot.periods:

        # 查詢目前已借數量
        reservations = ReservationList.objects.filter(
            date=start_date,
            periods=period,
            device=device
        )

        total_amount = 0

        for item in reservations:
            total_amount += item.amount

        # 檢查設備是否足夠
        if total_amount + amount > device.amount:

            return False

        # 建立預約
        ReservationList.objects.create(

            borrow_list=borrow,
            user=borrow.user,
            device=device,
            date=start_date,
            periods=period,
            amount=amount
        )

    return True


def submit_borrow(request):

    if request.method == 'POST':

        user_id = request.POST['user_id']

        device_id = request.POST['device_id']

        time_slot_id = request.POST['time_slot_id']

        device_amount = request.POST['device_amount']

        user = user.objects.get(id=user_id)

        device = device.objects.get(id=device_id)

        time_slot = time_slot.objects.get(id=time_slot_id)

        # 建立借用單
        borrow = submit_borrow.objects.create(

            user=user,

            device=device,

            time_slot=time_slot,

            device_amount=device_amount
        )

        # 建立預約
        success = create_reservation(borrow)

        if success:

            return HttpResponse("預約成功")

        else:

            borrow.delete()

            return HttpResponse("設備不足")

    return render(request, 'borrow.html')

def reservation_table(request):

    reservations = ReservationList.objects.all().order_by('date', 'periods')

    return render(request, 'reservation_list.html', {
        'reservations': reservations
    })