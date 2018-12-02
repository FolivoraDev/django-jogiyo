from django.urls import path

from ..apis import UserList

urlpatterns = [
    path('user/', UserList.as_view()),
]
