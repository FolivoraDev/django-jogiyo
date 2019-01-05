import datetime

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance as MeasureDistance
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from rest_framework import filters
from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from .models import Restaurant, Menu, Review, Order, Food, Category, SubChoice, Tag, Payment
from .serializer import RestaurantSerializer, MenuSerializer, ReviewSerializer, OrderSerializer, FoodSerializer, \
    CategorySerializer, SubChoiceSerializer, TagSerializer, PaymentSerializer, OrderCreateSerializer, \
    ReviewCreateSerializer, MenuCreateSerializer


class RestaurantList(generics.ListCreateAPIView):
    """
    get:
    음식점 목록을 불러옵니다. (리팩토링 예정)

    url parameter로 오름차순 내림차순 정렬이 가능합니다.
    'categories', 'tags', 'review_avg', 'review_count', 'min_order_amount', 'estimated_delivery_time'
    ex) restaurant/?ordering=categories
    ex) restaurant/?ordering=-categories

    url parameter에 lat, lng 값을 포함시키면 반경 1km이내 음식점을 불러옵니다.

    post:
    새로운 음식점을 생성합니다. (미완성)
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        lat = self.request.query_params.get('lat', False)
        lng = self.request.query_params.get('lng', False)

        # 위도 경도값을 get query parameter로 받아 반경 radius(km)안에 있는 음식점 목록을 조회합니다.
        if lat and lng:
            lat = float(lat)
            lng = float(lng)
            radius = 1
            point = Point(lng, lat)

            # query param ordering에 distance 문자열이 있을 경우 정렬 한 값을 조회합니다.
            distance = self.request.query_params.get('ordering', False)

            if distance:
                query = Restaurant.objects.filter(location__distance_lte=(point, MeasureDistance(km=radius))).annotate(
                    distance=Distance("location", point)).order_by(distance)
            else:
                query = Restaurant.objects.filter(location__distance_lte=(point, MeasureDistance(km=radius)))
        else:
            query = Restaurant.objects.filter(**self.kwargs)

        return query

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = (
        'categories', 'tags', 'review_avg', 'review_count', 'min_order_amount', 'estimated_delivery_time')


class RestaurantUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    get: 1개의 음식점에 대한 세부정보를 불러옵니다.
    put: 미완성
    patch: 미완성
    delete: 미완성
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('categories', 'tags', 'review_avg', 'review_count', 'min_order_amount', 'estimated_delivery_time')


class MenuList(generics.ListCreateAPIView):
    """
    get: restaurant_id에 해당하는 음식점의 메뉴를 불러옵니다.

    post: restaurant_id에 해당하는 음식점의 새로운 메뉴를 생성합니다.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(**self.kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MenuCreateSerializer
        return MenuSerializer

    def perform_create(self, serializer):
        serializer.save(**self.kwargs)


class MenuUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    미완성
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class ReviewList(generics.ListCreateAPIView):
    """
    get: restaurant_id에 해당하는 음식점의 리뷰목록을 불러옵니다.
    post: restaurant_id에 해당하는 음식점의 리뷰를 생성합니다.
    """
    queryset = Review.objects.all()
    lookup_url_kwarg = "restaurant_id"

    parser_classes = (MultiPartParser, CamelCaseJSONParser)

    def post(self, request, *args, **kwargs):
        print(request.data)
        # return HttpResponse('<img src = "%s" />' % request.data.get('review_images', 'qwlkejqlwej'))
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return Review.objects.filter(**self.kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        self.kwargs['user'] = self.request.user
        # 리뷰 평균을 계산합니다.
        self.kwargs['rating'] = (serializer.validated_data['rating_delivery'] +
                                 serializer.validated_data['rating_quantity'] +
                                 serializer.validated_data['rating_taste']) / 3

        date_from = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=1)

        # restuarant_id에 해당하는 음식점에서 요청한 유저의 주문 목록 중 24시간 이내에 가장 최근 것을 찾습니다.
        if self.kwargs['user'].order_set.exists():
            self.kwargs['menu_summary'] = [i for i in self.kwargs['user'].order_set.filter(
                restaurant__id=self.kwargs['restaurant'].id, time__gte=date_from).order_by(
                '-time').first().food.all().values_list(
                'id', flat=True)]

        serializer.save(**self.kwargs)

    filter_backends = (filters.OrderingFilter,)
    filter_fields = ('time',)


class ReviewUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """
    put: Review 인스턴스를 업데이트합니다.
    patch: Review 인스턴스를 일부 업데이트합니다.
    delete: Review 인스턴스를 삭제합니다.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer

    def get_queryset(self):
        return Review.objects.filter(**self.kwargs)

    filter_backends = (filters.OrderingFilter,)
    filter_fields = ('time',)


class OrderList(generics.ListCreateAPIView):
    """
    get: restaurant_id에 해당하는 음식점의 주문 목록을 불러옵니다.
    post: restaurant_id에 해당하는 음식점의 주문을 생성합니다. # 리팩토링 예정
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "restaurant_id"

    def get_queryset(self):
        return Order.objects.filter(**self.kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = OrderCreateSerializer
        request.data['restaurant'] = self.kwargs.get(self.lookup_url_kwarg)

        return self.create(request, *args, **kwargs)


class FoodList(generics.ListCreateAPIView):
    """
    get: DB에 있는 모든 음식을 불러옵니다.
    post: 새로운 음식을 생성합니다.
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_queryset(self):
        return Food.objects.filter(**self.kwargs)

    filter_backends = (DjangoFilterBackend,)


class CategoryList(generics.ListCreateAPIView):
    """
    get: DB에 있는 모든 카테고리를 불러옵니다.
    post: 새로운 카테고리를 생성합니다.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(**self.kwargs)


class SubChoiceList(generics.ListCreateAPIView):
    """
    get: DB에 있는 모든 추가메뉴를 불러옵니다.
    post: 새로운 추가메뉴를 생성합니다. # 미완성
    """
    queryset = SubChoice.objects.all()
    serializer_class = SubChoiceSerializer

    def get_queryset(self):
        return SubChoice.objects.filter(**self.kwargs)


class TagList(generics.ListCreateAPIView):
    """
    get: DB에 있는 모든 태그를 불러옵니다.
    post: 새로운 태그를 생성합니다.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PaymentList(generics.ListCreateAPIView):
    """
    get: DB에 있는 모든 결제방식을 불러옵니다.
    post: 새로운 결제방식을 생성합니다.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
