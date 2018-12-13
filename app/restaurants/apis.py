from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Restaurant, Menu, Review, Order, Food, Category, SubChoice, Tag, Payment
from .serializer import RestaurantSerializer, MenuSerializer, ReviewSerializer, OrderSerializer, FoodSerializer, \
    CategorySerializer, SubChoiceSerializer, TagSerializer, PaymentSerializer, OrderCreateSerializer, \
    ReviewCreateSerializer


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(**self.kwargs)

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('categories', 'tags')


class RestaurantUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuList(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(**self.kwargs)


class MenuUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_url_kwarg = "restaurant_id"

    def get_queryset(self):
        return Review.objects.filter(**self.kwargs)

    def post(self, request, *args, **kwargs):
        """
        해당 레스토랑에 대한 리뷰 생성입니다.

        *"comment":"string",
        *"rating_delivery": int,
        *"rating_quantity": int,
        *"rating_taste": int

        """
        self.serializer_class = ReviewCreateSerializer
        rating_delivery = request.data.get('rating_delivery', 0)
        rating_quantity = request.data.get('rating_quantity', 0)
        rating_taste = request.data.get('rating_taste', 0)

        request.data['rating'] = (rating_delivery + rating_quantity + rating_taste) / 3
        request.data['restaurant'] = self.kwargs.get(self.lookup_url_kwarg)
        return self.create(request, *args, **kwargs)


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


class FoodFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Food
        fields = ['id', 'min_price', 'max_price']


class FoodList(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_queryset(self):
        return Food.objects.filter(**self.kwargs)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = FoodFilter


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
