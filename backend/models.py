from django.db import models
from django.contrib.auth.models import AbstractUser


class M_User(AbstractUser):
    full_name=models.CharField(max_length=255)
    usertype= models.CharField(max_length=30)
    email=models.EmailField(max_length=50,null=True, blank=True)
    password=models.CharField(max_length=10,null=True, blank=True)
  

class restaurant(models.Model):
      user = models.OneToOneField(M_User,on_delete=models.CASCADE,null=True)
      restaurant_name=models.CharField(max_length=255)
      restaurant_owner=models.CharField(max_length=255,null=True)
      owner_number=models.IntegerField(unique=True,null=True)
      owner_email=models.EmailField(max_length=254,unique=True,null=True)
      restaurant_desc=models.CharField(max_length=255,default="null")
      restaurant_address=models.CharField(max_length=255,default="null")
      



class comments(models.Model):
      user_id=models.ForeignKey(M_User,on_delete=models.CASCADE,null=True)
      restaurant_id=models.ForeignKey(restaurant,on_delete=models.CASCADE)
      Review=models.TextField()



class Leaderborad_backup(models.Model):
      restaurant_name=models.CharField(max_length=255)
      score=models.CharField(max_length=255)
      