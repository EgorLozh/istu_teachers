from django.urls import path
from .views import Whos_hotter, Full_bd, Rating


urlpatterns = [
    path('', Whos_hotter.as_view(), name='whos_hotter'),
    path('rating/', Rating.as_view(), name = 'rating')
    # path('full_bd', Full_bd.as_view())
]