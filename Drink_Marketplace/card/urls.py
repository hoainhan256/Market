# card/urls.py

from django.urls import path
from . import views

app_name = 'card'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('history/', views.purchase_history, name='history'),
    path('checkout/', views.checkout, name='checkout'),
]
