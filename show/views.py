from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from datetime import date, datetime
from django.views.generic import ListView
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
        
        return context