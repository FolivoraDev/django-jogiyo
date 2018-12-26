from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance as MeasureDistance
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics

from .models import Restaurant, Menu, Review, Order, Food, Category, SubChoice, Tag, Payment
from .serializer import RestaurantSerializer, MenuSerializer, ReviewSerializer, OrderSerializer, FoodSerializer, \
    CategorySerializer, SubChoiceSerializer, TagSerializer, PaymentSerializer, OrderCreateSerializer, \
    ReviewCreateSerializer, MenuCreateSerializer


class RestaurantList(generics.ListCreateAPIView):
    """
    get:
    음식점 목록을 불러옵니다.

    post:
    새로운 음식점을 생성합니다.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        lat = self.request.query_params.get('lat', False)
        lng = self.request.query_params.get('lng', False)

        if lat and lng:
            lat = float(lat)
            lng = float(lng)
            radius = 1
            point = Point(lng, lat)

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
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('categories', 'tags', 'review_avg', 'review_count', 'min_order_amount', 'estimated_delivery_time')


class MenuList(generics.ListCreateAPIView):
    """
    get:
    DB에 있는 모든 메뉴를 불러옵니다.

    post:
    새로운 메뉴를 생성합니다.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    lookup_field = 'restaurant_id'
    lookup_url_kwarg = 'restaurant_id'

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
      get:
      restuarant id에 대한 음식점을 불러옵니다.

      put:
      restuarant id에 대한 음식점을 업데이트합니다.

      patch:
      restuarant id에 대한 음식점을 일부 업데이트합니다.

      delete:
      restuarant id에 대한 음식점을 삭제합니다.

    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_url_kwarg = "restaurant_id"

    def get_queryset(self):
        return Review.objects.filter(**self.kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = ReviewCreateSerializer

        rating_delivery = request.data.get('rating_delivery', 0)
        rating_quantity = request.data.get('rating_quantity', 0)
        rating_taste = request.data.get('rating_taste', 0)

        request.data['rating'] = (rating_delivery + rating_quantity + rating_taste) / 3
        request.data['restaurant'] = self.kwargs.get(self.lookup_url_kwarg)
        return self.create(request, *args, **kwargs)

    filter_backends = (filters.OrderingFilter,)
    filter_fields = ('time',)


class ReviewUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "restaurant_id"

    def get_queryset(self):
        return Order.objects.filter(**self.kwargs)

    def post(self, request, *args, **kwargs):
        """
        음식점(restaurant_id)의 주문 목록을 생성합니다
            (*: 필수로 입력해야 하는 값입니다.)
            user: 주문한 사람 (헤더의 토큰)
            restaurant: 주문한 음식점 (url의 parameter restaurant_id)
            food: 주문한 음식 (음식의 id값을 리스트로 넣으시면 됩니다. ex) [1,2,3])
            time: 주문한 시간 (주문이 생성될때 자동입력)
            *address: 주소
            request: 요청 사항
        """

        self.serializer_class = OrderCreateSerializer
        request.data['restaurant'] = self.kwargs.get(self.lookup_url_kwarg)

        return self.create(request, *args, **kwargs)


class FoodList(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_queryset(self):
        return Food.objects.filter(**self.kwargs)

    filter_backends = (DjangoFilterBackend,)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(**self.kwargs)


class SubChoiceList(generics.ListCreateAPIView):
    queryset = SubChoice.objects.all()
    serializer_class = SubChoiceSerializer

    def get_queryset(self):
        return SubChoice.objects.filter(**self.kwargs)


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
