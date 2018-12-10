from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Restaurant, Menu, Review, Order, Food, Category, SubChoice, Tag, Payment
from .serializer import RestaurantSerializer, MenuSerializer, ReviewSerializer, OrderSerializer, FoodSerializer, \
    CategorySerializer, SubChoiceSerializer, TagSerializer, PaymentSerializer


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

    def get_queryset(self):
        return Review.objects.filter(**self.kwargs)


class ReviewUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(**self.kwargs)


class FoodList(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubChoiceList(generics.ListCreateAPIView):
    queryset = SubChoice.objects.all()
    serializer_class = SubChoiceSerializer


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
