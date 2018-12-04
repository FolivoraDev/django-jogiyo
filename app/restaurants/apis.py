from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Restaurant
from .serializer import RestaurantSerializer


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('categories', 'tags')
