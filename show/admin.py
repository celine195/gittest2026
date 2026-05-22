from django.contrib import admin

# Register your models here.


from django.contrib import admin
# 引入你寫好的所有 Model（這裡配合你目前的命名）
from .models import reservationlist as ReservationList 
from .models import Borrowlist 

# 如果你還有寫 time 或 device 的 model，記得也要一起引入，例如：
# from .models import TimeSlot, Device

# 把它們註冊到 Django 管理系統中
admin.site.register(Borrowlist)
admin.site.register(ReservationList)
