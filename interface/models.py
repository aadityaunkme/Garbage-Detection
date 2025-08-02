from django.db import models
from django.contrib.auth.models import User

class User_detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_detail')
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=13)

class Media(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='pictures', blank=True)
    status = models.BooleanField(default=False)



