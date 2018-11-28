from django.urls import path, include

from ..apis import UserList

urlpatterns = [
    path('', UserList.as_view()),
    path('api/', include('members.urls.api'))
]
