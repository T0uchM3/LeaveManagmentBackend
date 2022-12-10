from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime    
from django.utils.timezone import now


class CustomUser(AbstractUser):
    #username = models.DateTimeField(auto_now_add=True,blank=True)
    username = models.CharField(max_length=150,unique=True,blank=True)
    userfirstname = models.CharField(max_length=50)
    userlastname = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    #leaveid = models.ForeignKey('Leave', on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    paternity = models.IntegerField(max_length=50,default=0)
    maternity = models.IntegerField(max_length=50,default=0)
    paid = models.IntegerField(max_length=50,default=30)
    rtt = models.IntegerField(max_length=50,default=0)
    def __int__(self):
        return self.id

class Leave(models.Model):
    startdate= models.DateTimeField(auto_now_add=True,blank=True)
    enddate = models.DateTimeField(auto_now_add=True,blank=True)
    days = models.IntegerField(max_length=50,default=0)
    leavetype = models.CharField(max_length=100,default="")
    userid = models.IntegerField(max_length=50,default=0)
    status = models.CharField(max_length=100,default="")

    def __int__(self):
        return self.id


# when adding new field
# run python manage.py migrate --run-syncdb