from django.db import models
from django.contrib.auth.models import AbstractUser
# from numpy import require
# from setuptools import Require
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        # nickname 필드를 추가
        nickname = data.get("nickname")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
            self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user

# Create your models here.


class User(AbstractUser):
    # deposit_fin_prdt_cd = models.ForeignKey(
    #     DepositProduct, on_delete=models.CASCADE,
    #     related_name='deposit', null=True, blank=True)  # 금융상품 코드
    # saving_fin_prdt_cd = models.ForeignKey(
    #     SavingProduct, on_delete=models.CASCADE,
    #     related_name='saving', null=True, blank=True)
    nickname = models.CharField(max_length=10, null=False, unique=True)
    email = models.EmailField(
        max_length=255, null=True, unique=True)  # 일단 null=True
    GENDERS = (('M', '남성(Man)'), ('W', '여성(Woman)'))
    gender = models.CharField(
        verbose_name='성별', max_length=1, choices=GENDERS, null=False)  # null=True
    age = models.IntegerField(null=True, default=-1)  # null=True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

# 유저와 게시판의 1:M관계를 가지고 있는 모델


class Board(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="boards"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

