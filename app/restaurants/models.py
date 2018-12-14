from django.contrib.auth import get_user_model

# Create your models here.
from django.contrib.gis.db.models import PointField
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=200, unique=True)  # 이름
    logo_url = models.ImageField(blank=True, null=True, upload_to='restaurant')  # 로고
    review_avg = models.DecimalField(max_digits=10, decimal_places=2)  # 평점
    min_order_amount = models.IntegerField()  # 배달 최소 주문 금액
    except_cash = models.BooleanField(default=True)  # 현금 결제
    payment_methods = models.ManyToManyField('Payment', blank=True)  # 결제 방식
    review_count = models.IntegerField()  # 리뷰 개수 (삭제예정)
    owner_reply_count = models.IntegerField()  # 사장 리뷰 개수 (삭제예정)
    estimated_delivery_time = models.CharField(max_length=20)  # 걸리는 시간
    discount_percent = models.IntegerField()  # 할인
    additional_discount_per_menu = models.IntegerField()  # 배달할인
    delivery_fee = models.IntegerField(default=0)  # 배달료

    begin = models.TimeField()  # 영업 시작
    end = models.TimeField()  # 영업 끝
    company_name = models.CharField(max_length=50)  # 사업장 이름
    company_number = models.CharField(max_length=20)  # 사업장 번호
    country_origin = models.CharField(max_length=2000)  # 원산지

    introduction_text = models.CharField(max_length=500, default='')  # 사장님 알림

    tags = models.ManyToManyField('Tag', blank=True)  # 태그(세스코)
    categories = models.ManyToManyField('Category', blank=True)  # 카테고리

    lat = models.DecimalField(max_digits=15, decimal_places=12, default=0)  # 위도
    lng = models.DecimalField(max_digits=15, decimal_places=12, default=0)  # 경도

    location = PointField(default='POINT(0.0 0.0)')


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # 주문한 사람
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)  # 주문한 음식점
    food = models.ManyToManyField('Food', blank=True)  # 주문한 음식
    time = models.DateTimeField(auto_now=True)  # 주문한 시간
    address = models.CharField(max_length=255)  # 주소
    request = models.CharField(max_length=200, blank=True)  # 요청 사항


class Food(models.Model):
    name = models.CharField(max_length=200, unique=True)  # 이름
    image = models.ImageField(blank=True, null=True, upload_to='restaurant/food', max_length=255)  # 이미지
    price = models.IntegerField()  # 가격

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'


class Menu(models.Model):
    name = models.CharField(max_length=200)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    food = models.ManyToManyField('Food', blank=True)


class SubChoice(models.Model):
    name = models.CharField(max_length=200, unique=True)
    food = models.ManyToManyField('Food', blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Payment(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Review(models.Model):
    comment = models.CharField(max_length=500)  # 댓글
    rating = models.DecimalField(max_digits=10, decimal_places=1)  # 평균
    rating_delivery = models.DecimalField(max_digits=10, decimal_places=1)  # 배달
    rating_quantity = models.DecimalField(max_digits=10, decimal_places=1)  # 양
    rating_taste = models.DecimalField(max_digits=10, decimal_places=1)  # 맛
    review_images = models.ImageField(blank=True, null=True, upload_to='restaurant/review')
    time = models.DateTimeField(auto_now=True)  # 작성시간
    menu_summary = models.ManyToManyField('Food', blank=True)  # 주문한 메뉴
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # 작성자
