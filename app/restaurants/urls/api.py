from django.urls import path

from ..apis import RestaurantList, MenuList, ReviewList, RestaurantUpdateView, OrderList, FoodList, CategoryList, \
    SubChoiceList, PaymentList, TagList

urlpatterns = [
    # 각종 모델 / GET, POST 요청 가능
    path('restaurant/', RestaurantList.as_view()),
    path('food/', FoodList.as_view()),
    path('menu/', MenuList.as_view()),
    path('subchoice/', SubChoiceList.as_view()),
    path('category/', CategoryList.as_view()),
    path('tag/', TagList.as_view()),
    path('payment/', PaymentList.as_view()),

    # 특정 레스토랑(pk값)의 정보 / GET, PUT, PATCH, DELETE 요청 가능
    path('<int:pk>/restaurant/', RestaurantUpdateView.as_view()),
    path('<int:pk>/info/', RestaurantUpdateView.as_view()),

    # 특정 레스토랑(restaurant_id)에 대한 메뉴, 리뷰, 주문 / GET, POST 요청 가능
    path('<int:restaurant_id>/menu/', MenuList.as_view()),
    path('<int:restaurant_id>/review/', ReviewList.as_view()),
    path('<int:restaurant_id>/order/', OrderList.as_view()),
]
