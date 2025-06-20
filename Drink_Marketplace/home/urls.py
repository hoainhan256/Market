from django.urls import path
from home import views as home
from . import views


urlpatterns = [
   path('',home.Get_home, name="home"),
   path('product/<int:id>/', views.product_detail, name='product_detail'),
   path('admins/messages/', views.support_messages, name='support_message'),
   path('admins/messages/update/<int:comment_id>/', views.update_comment_status, name='update_comment_status'),
]