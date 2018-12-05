from django.urls import path, include

from ..views import crawler, detail_crawler

urlpatterns = [
    path('crawling/', crawler),
    path('dc/', detail_crawler),
    path('api/', include('restaurants.urls.api'))
]
