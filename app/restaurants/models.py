from django.db import models


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50, unique=True)         #이름
    logo_url = models.ImageField(blank=True, null=True, upload_to='restaurant') #로고
    review_avg = models.IntegerField()                          #평점
    min_order_amount = models.IntegerField()                    #배달 최소 주문
    review_count = models.IntegerField()                        #리뷰 개수
    payment = models.BooleanField(default=True)                 #요기서 결제
    estimated_delivery_time = models.CharField(max_length=20)   #걸리는 시간
    additional_discount_per_menu = models.IntegerField()        #배달할인
    tags = models.CharField(max_length=20)                      #태그(세스코)
