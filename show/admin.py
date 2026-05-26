from django.contrib import admin

from django.contrib import admin
# 引入你 show/models.py 裡面定義的兩個資料模型
from .models import Borrowlist , device, time, devicecar
from .models import reservationlist as ReservationList

class BorrowlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'start_date', 'get_day_display', 'get_periods_display', 'location', 'status')
    list_filter = ('status', 'periods', 'day')

class TimeAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'start_date', 'end_date', 'show_day_chinese', 'show_periods_chinese')
    list_filter = ('day', 'periods')

    @admin.display(description='星期')
    def show_day_chinese(self, obj):
        return obj.get_day_display()

    @admin.display(description='預約節次') 
    def show_periods_chinese(self, obj):
        return obj.get_periods_display()

admin.site.register(Borrowlist, BorrowlistAdmin)
admin.site.register(ReservationList)
admin.site.register(device)          
admin.site.register(time, TimeAdmin)           
admin.site.register(devicecar)
