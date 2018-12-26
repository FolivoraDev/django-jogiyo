from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from members.models import User
from .serializer import UserSerializer


@permission_classes((AllowAny,))
class UserList(generics.ListCreateAPIView):
    """
    get: Header에 포함 된 토큰으로 유저를 찾아 유저에 대한 정보를 반환합니다.
    post: 새로운 유저를 생성하고 생성에 성공하면 유저 정보를 반환합니다.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)
