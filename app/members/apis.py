from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .serializer import UserSerializer


@permission_classes((AllowAny,))
class UserList(generics.ListCreateAPIView):
    """
    get: 전체 유저를 정보를 반환합니다. (user/me/ 현재유저) (user/pk/ pk유저)
    post: 새로운 유저를 생성하고 생성에 성공하면 유저 정보를 반환합니다.
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        who = self.kwargs.get('me')

        if who is not None:
            if who == 'me':
                queryset = get_user_model().objects.filter(username=self.request.user)
            else:
                queryset = get_user_model().objects.filter(pk=who)

        return queryset
