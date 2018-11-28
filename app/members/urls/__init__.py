from django.urls import path

from ..apis import UserList

urlpatterns = [
    path('', UserList.as_view())
]
