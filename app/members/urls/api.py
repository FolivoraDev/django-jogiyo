from django.urls import path

from restaurants.apis import OrderList
from ..apis import UserList

urlpatterns = [
    # 유저 정보 / GET, POST 요청 가능
    path('user/', UserList.as_view()),
    path('user/<str:me>/', UserList.as_view()),
    # path('user/me/', UserDetailView.as_view()),
    # path('user/me/', UserList.as_view()),
    # path('<int:pk>/user/', UserList.as_view()),

    # 특정 유저(pk)에 대한 주문 목록
    path('<int:user_id>/order/', OrderList.as_view()),
]
