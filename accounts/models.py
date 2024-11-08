from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    phone_number = models.TextField()
    GENDER = (('M', '남성(Men)'), ('W','여성(Women)'))
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDER)
    age = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
