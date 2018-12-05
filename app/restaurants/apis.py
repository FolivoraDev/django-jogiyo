from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response

from .models import Restaurant
from .serializer import RestaurantSerializer, RestaurantDetailSerializer


class RestaurantList(RetrieveModelMixin, generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('categories', 'tags')

    def get(self, request, *args, **kwargs):
        restaurant_id = request.GET.get('id')
        if restaurant_id:
            self.queryset = Restaurant.objects.filter(id=restaurant_id)
            self.serializer_class = RestaurantDetailSerializer

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
