from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from ..apis import UserList

schema_view = get_swagger_view(title='Members API')

urlpatterns = [
    path('userlist/', UserList.as_view()),
    path('testing/', schema_view)
]
