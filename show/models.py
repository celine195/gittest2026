from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User

# Create your models here.

class user(models.Model):
    name = models.CharField("姓名",max_length= 10)
    email = models.CharField("信箱",max_length= 100)
    ROLE_CHOICES = (
        ('teacher', '老師'),
        ('student', '學生'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')


class Borrowlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="借用人")
    phone = models.CharField("連絡電話",max_length= 25)

    #這
    usage_type_choices = (
        ('once','單次'),
        ('weekly','每周'),
    )
    usage_type = models.CharField(max_length=10, choices=usage_type_choices, default='once')
    
    AMOUNT_CHOICES=(
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('one', '1'),
        ('two', '2'),
        ('three', '3'),
        ('four', '4'),
        ('five', '5'),
    )   
    
    quantity = models.IntegerField(default=1, verbose_name="設備數量")
    device_id = models.CharField(max_length=50, default='1', verbose_name="設備ID")
    #device_amount = models.PositiveIntegerField(choices=AMOUNT_CHOICES, default=1)
    time_id = models.CharField(max_length=20, default='1', verbose_name="時間ID")
    
    
    
class time(models.Model):
    start_date = models.DateField("開始日期",null=True, blank=True)
    end_date = models.DateField("結束日期",null=True, blank=True)
    PERIODS_CHOICES =(
        ('1','第一節'),
        ('2','第二節'),
        ('3','第三節'),
        ('4','第四節'),
        ('5','第五節'),
        ('6','第六節'),
        ('7','第七節'),
        ('8','第八節'),
        ('4.5','午休'),
    )
    periods = models.CharField(
        choices=PERIODS_CHOICES,
        max_length=50, 
        verbose_name="節次")
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
    
    device_type_choices = ()
    device_type = models.CharField(max_length=10, choices=device_type_choices, default='')
    amount = models.IntegerField(max_length=10)
    #尚未填寫種類
    

class devicecar(models.Model):
    device_id = models.CharField(
        max_length=100, 
        )
    device_amount = models.PositiveIntegerField(default=1)

class reservationlist(models.Model):
    #list_id = models.IntegerField
    #date = models.DateField
    #time_id = models.IntegerField
    #device_id = models.IntegerField
    #devicecar_id = models.IntegerField

    
    borrow_list = models.ForeignKey(
        'BorrowList',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )

    device = models.ForeignKey(
        'Device',
        on_delete=models.CASCADE
    )

    date = models.DateField()

    periods = models.CharField(max_length=20)

    amount = models.PositiveIntegerField(default=1)
    
