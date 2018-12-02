from django.urls import path

from ..apis import RestaurantList

urlpatterns = [
    path('restaurant/', RestaurantList.as_view()),
]
