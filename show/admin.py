from django.contrib import admin

# Register your models here.
from django.contrib import admin
# 引入你 show/models.py 裡面定義的兩個資料模型
from .models import Borrowlist
from .models import reservationlist as ReservationList

# 把這兩個資料模型註冊到 Django 管理後台
admin.site.register(Borrowlist)
admin.site.register(ReservationList)