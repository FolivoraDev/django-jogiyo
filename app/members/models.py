from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models


class User(AbstractUser):
    # admin에서 이 필드를 수정할 수 있도록 설정
    img_profile = models.ImageField(upload_to='user', blank=True)

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = verbose_name + ' 목록'
