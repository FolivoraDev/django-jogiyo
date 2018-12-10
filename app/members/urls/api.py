from django.urls import path

from restaurants.apis import OrderList
from ..apis import UserList

urlpatterns = [
    path('user/', UserList.as_view()),
    path('<int:pk>/user/', UserList.as_view()),
    path('<int:user_id>/order/', OrderList.as_view()),
]
