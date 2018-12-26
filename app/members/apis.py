from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from members.models import User
from .serializer import UserSerializer


@permission_classes((AllowAny,))
class UserList(generics.ListCreateAPIView):
    """
    get:
    DB에 존재하는 모든 유저를 보여줍니다.

    post:
    새로운 유저 인스턴스를 생성합니다.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)

    def post(self, request, *args, **kwargs):

        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username or not password:
            return Response('username 혹은 password를 올바르게 입력하세요', status=status.HTTP_400_BAD_REQUEST)

        try:
            new_user = get_user_model().objects.create_user(username=username, password=password)
        except Exception as e:
            print(e.__context__)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=UserSerializer(new_user).data, status=status.HTTP_200_OK)
