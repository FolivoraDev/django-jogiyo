from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializer import UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    Post

    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer