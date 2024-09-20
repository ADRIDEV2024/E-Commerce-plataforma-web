from django.contrib import admin 
from django.urls import path
from .views_2 import LoginView, LogoutView, SignupView
from .views import ( products, CheckoutView, HomeView, OrderSummaryView,
    add_to_cart, remove_from_cart, remove_single_item_from_cart, PaymentView,
    AddCouponView, RequestRefundView )




url_patterns = [
    
    path("", HomeView.as_view(), name='home'),
    path('store', store, name='store'), 
    path('signup', SignupView.as_view(), name='signup'), 
    path('login', LoginView.as_view(), name='login'), 
    path('logout', LogoutView.as_view(), name='logout'), 
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', products, name='products'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')

]
