from django.urls import path
from . import views

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('/home', views.store, name = 'home'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('updatecart', views.updateCart),
    path('updatequantity', views.updateQuantity),
    path('payment', views.payment, name = 'payment'),
    path('login/',views.LoginPage,name='login'),
    path('logout/',views.LoginPage,name='logout')
]