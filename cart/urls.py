from django.urls import path as url
from . import views

app_name = 'cart'

urlpatterns = [
    url('', views.cart_detail, name='cart_detail'),
    url('add/<int:product_id>', views.cart_add, name='cart_add'),
    url('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    url('order', views.order, name='order'),
    url('confirm-order', views.confirm_order, name='confirm_order'),
    url('pay/<int:orderid>', views.pay, name='pay'),
    url('payment/<int:orderid>', views.payment, name='payment'),
]
