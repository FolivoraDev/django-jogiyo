from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=200, unique=True)  # 이름
    logo_url = models.ImageField(blank=True, null=True, upload_to='restaurant')  # 로고
    review_avg = models.DecimalField(max_digits=10, decimal_places=2)  # 평점
    min_order_amount = models.IntegerField()  # 배달 최소 주문 금액
    except_cash = models.BooleanField(default=True)  # 현금 결제
    payment_methods = models.ManyToManyField('Payment', blank=True)  # 결제방
    review_count = models.IntegerField()  # 리뷰 개수
    owner_reply_count = models.IntegerField()  # 사장 리뷰 개수
    estimated_delivery_time = models.CharField(max_length=20)  # 걸리는 시간
    discount_percent = models.IntegerField()  # 할인
    additional_discount_per_menu = models.IntegerField()  # 배달할인

    begin = models.TimeField()  # 영업 시작
    end = models.TimeField()  # 영업 끝
    company_name = models.CharField(max_length=50)  # 사업장 이름
    company_number = models.CharField(max_length=20)  # 사업장 번호
    country_origin = models.CharField(max_length=2000)  # 원산지

    tags = models.ManyToManyField('Tag', blank=True)  # 태그(세스코)
    categories = models.ManyToManyField('Category', blank=True)  # 카테고리


class Food(models.Model):
    name = models.CharField(max_length=200, unique=True)  # 이름
    image = models.ImageField(blank=True, null=True, upload_to='restaurant/food', max_length=255)  # 이미지
    price = models.IntegerField()  # 가격


class Menu(models.Model):
    name = models.CharField(max_length=200)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    food = models.ManyToManyField('Food', blank=True)


class SubChoice(models.Model):
    name = models.CharField(max_length=200, unique=True)
    food = models.ManyToManyField('Food', blank=True)


# class Additional_Menu(models)


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Payment(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Review(models.Model):
    comment = models.CharField(max_length=500)
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    rating_delivery = models.DecimalField(max_digits=10, decimal_places=1)
    rating_quantity = models.DecimalField(max_digits=10, decimal_places=1)
    rating_taste = models.DecimalField(max_digits=10, decimal_places=1)
    review_images = models.ImageField(blank=True, null=True, upload_to='restaurant/review')
    time = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
