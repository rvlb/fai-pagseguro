from django.urls import path
from .views import IndexView, CartView, add_to_cart

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('cart', CartView.as_view(), name='cart'),
    path('add_cart', add_to_cart, name='add_cart'),
]