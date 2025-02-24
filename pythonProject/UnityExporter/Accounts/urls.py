# accounts/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),


    path('items/', views.items_view, name='items_view'),  # View all items
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),  # Add item to cart
    path('cart/', views.cart_view, name='cart_view'),  # View cart
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
  # Remove item from cart

path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),

]
