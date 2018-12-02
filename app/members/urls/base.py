from django.urls import path, include

from ..apis import UserList

urlpatterns = [
    path('api/', include('members.urls.api'))
]
