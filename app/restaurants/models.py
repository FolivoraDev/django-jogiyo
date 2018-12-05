from django.db import models


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 이름
    logo_url = models.ImageField(blank=True, null=True, upload_to='restaurant')  # 로고
    review_avg = models.DecimalField(max_digits=10, decimal_places=2)  # 평점
    min_order_amount = models.IntegerField()  # 배달 최소 주문
    review_count = models.IntegerField()  # 리뷰 개수
    payment = models.BooleanField(default=True)  # 요기서 결제
    estimated_delivery_time = models.CharField(max_length=20)  # 걸리는 시간
    additional_discount_per_menu = models.IntegerField()  # 배달할인
    tags = models.ManyToManyField('Tag', blank=True)  # 태그(세스코)
    categories = models.ManyToManyField('Category', blank=True)  # 카테고리


class Food(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 이름
    image = models.ImageField(blank=True, null=True, upload_to='restaurant/food')  # 이미지
    price = models.IntegerField()  # 가격
    subchoices = models.ManyToManyField('Menu', blank=True)  # 추가메뉴


class Menu(models.Model):
    name = models.CharField(max_length=20, unique=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

# class Additional_Menu(models)


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
