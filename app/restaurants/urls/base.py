from django.urls import path, include

urlpatterns = [
    # path('crawling/', crawler),
    # path('dc/', detail_crawler),
    # path('nc/', new_crawler),
    path('api/', include('restaurants.urls.api'))
]
