from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Restaurant, Menu, Review
from .serializer import RestaurantSerializer, MenuSerializer, ReviewSerializer


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(**self.kwargs)

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('categories', 'tags')


class MenuList(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        return Menu.objects.filter(**self.kwargs)


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(**self.kwargs)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer


class InfoList(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(**self.kwargs)
