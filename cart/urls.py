from django.urls import path
from .views import AddtoCart, CartItems, AddCoupon

urlpatterns = [
    path('add-to-cart/<int:product_id>', AddtoCart.as_view(), name='add-to-cart'),
    path('cart/', CartItems.as_view(), name='cart'),
    path('add-coupon/', AddCoupon.as_view(), name='add-coupon'),
]
