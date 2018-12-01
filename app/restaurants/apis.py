
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from config.settings.base import MEDIA_URL, MEDIA_ROOT
from .models import Restaurant
from .serializer import RestaurantSerializer


class RestaurantList(generics.ListCreateAPIView):
    """
    get:
    DB에 존재하는 모든 유저를 보여줍니다.

    post:
    새로운 유저 인스턴스를 생성합니다.
    """

    print(MEDIA_ROOT)

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

