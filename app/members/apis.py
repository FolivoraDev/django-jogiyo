from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializer import UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    get:
    DB에 존재하는 모든 유저를 보여줍니다.

    post:
    새로운 유저 인스턴스를 생성합니다.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
