from django.urls import path
from home import views as home
from . import views


urlpatterns = [
   path('',home.Get_home, name="home"),
   path('product/<int:id>/', views.product_detail, name='product_detail'),
   
]