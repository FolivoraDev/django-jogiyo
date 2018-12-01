from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from ..apis import RestaurantList

schema_view = get_swagger_view(title='Restaurants API')

urlpatterns = [
    path('restaurant/', RestaurantList.as_view()),
    path('docs/', schema_view)
]
