from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # admin에서 이 필드를 수정할 수 있도록 설정

    nick_name = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = verbose_name + ' 목록'
