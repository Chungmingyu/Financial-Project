from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
# from numpy import require
# from setuptools import Require


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(
        max_length=10,
        null=True,
        unique=True
    )
    email = models.EmailField(max_length=255, unique=True)
    GENDERS = (('M', '남성(Man)'), ('W', '여성(Woman)'))
    gender = models.CharField(
        verbose_name='성별', max_length=1, choices=GENDERS, null=False)
    age = models.IntegerField(null=False, default=-1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
