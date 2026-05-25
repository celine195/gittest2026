from django.contrib import admin

from django.contrib import admin
from .models import Borrowlist
from .models import reservationlist as ReservationList

admin.site.register(Borrowlist)
admin.site.register(ReservationList)