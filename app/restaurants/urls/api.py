from django.urls import path

from ..apis import RestaurantList, MenuList, ReviewList, InfoList

urlpatterns = [
    path('restaurant/', RestaurantList.as_view()),
    path('<int:pk>/info/', InfoList.as_view()),
    path('<int:restaurant_id>/menu/', MenuList.as_view()),
    path('<int:restaurant_id>/review/', ReviewList.as_view()),
]
