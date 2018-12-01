from django.urls import path, include

from ..views import crawler

urlpatterns = [
    path('crawling/', crawler),
    path('api/', include('restaurants.urls.api'))
]
