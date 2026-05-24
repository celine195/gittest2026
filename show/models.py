from django.db import models
from datetime import timedelta

# Create your models here.

class user(models.Model):
    name = models.CharField("姓名",max_length= 10)
    email = models.CharField("信箱",max_length= 100)
    ROLE_CHOICES = (
        ('teacher', '老師'),
        ('administrator','圖書館管理員'),
        ('student', '學生'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='student')


class list(models.Model):
    user_id = models.IntegerField("借用人")
    phone = models.CharField("連絡電話",max_length= 25)

    #這
    usage_type_choices = (
        ('once','單次'),
        ('weekly','每周'),
    )
    usage_type = models.CharField(max_length=10, choices=usage_type_choices, default='once')
    device_id = models.IntegerField()
    AMOUNT_CHOICES = (
        ('1', '1台'),
        ('2', '2台'),
        ('3', '3台'),
        ('4', '4台'),
        ('5', '5台'),
        ('6', '6台'),
        ('7', '7台'),
        ('8', '8台'),
        ('9', '9台'),
        ('10', '10台'),
        ('11', '11台'),
        ('12', '12台'),
        ('13', '13台'),
        ('14', '14台'),
        ('15', '15台'),
        ('16', '16台'),
        ('17', '17台'),
        ('18', '18台'),
        ('19', '19台'),
        ('20', '20台'),
        ('21', '21台'),
        ('22', '22台'),
        ('23', '23台'),
        ('24', '24台'),
        ('25', '25台'),
        ('26', '26台'),
        ('27', '27台'),
        ('28', '28台'),
        ('29', '29台'),
        ('30', '30台'),
        ('31', '31台'),
        ('32', '32台'),
        ('33', '33台'),
        ('34', '34台'),
        ('35', '35台'),
        ('one', '1車'),
        ('two', '2車'),
        ('three', '3車'),
        ('four', '4車'),
        ('five', '5車'),
    )
    device_amount = models.PositiveIntegerField(choices=AMOUNT_CHOICES, default=1)
    time_id = models.IntegerField()
    classroom = models.CharField(max_length = 10)
    
    
class time(models.Model):
    start_date = models.DateField("開始日期",null=True, blank=True)
    end_date = models.DateField("結束日期",null=True, blank=True)
    PERIODS_CHOICES = (
        ('1', '第一節'),
        ('2', '第二節'),
        ('3', '第三節'),
        ('4', '第四節'),
        ('5', '第五節'),
        ('6', '第六節'),
        ('7', '第七節'),
        ('8', '第八節'),
        ('4.5', '午休'),
    )
    periods = models.CharField(
        max_length=50, 
        choices=PERIODS_CHOICES, 
        verbose_name="節次",
        default='1'
    )
    DAY_CHOICES = (
        ('Monday','星期一'),
        ('Tuesday','星期二'),
        ('Wednesday','星期三'),
        ('Thursday','星期四'),
        ('Friday','星期五'),
    )
    day = models.CharField(
        choices=DAY_CHOICES,
        max_length=50, 
        verbose_name="星期")

class device(models.Model):
    device_type_choices =(
        ('iPad', 'iPad'),
        ('Chromebook', 'Chromebook'), 
        ('SurfaceGo', 'Surface Go'), 
        ('Acer', 'Acer小筆電'),
    )
    device_type = models.CharField(max_length=10, choices=device_type_choices, default='iPad')
    amount = models.IntegerField()

class devicecar(models.Model):
    device_id = models.CharField(
        max_length=100, 
        )
    device_amount = models.PositiveIntegerField(default=1)

class reservationlist(models.Model):
    list_id = models.IntegerField()
    date = models.DateField()
    time_id = models.IntegerField()
    device_id = models.IntegerField()
    devicecar_id = models.IntegerField()
    
