from django.urls import path as url
from . import views

urlpatterns = [
    url('catalog/', views.product_list, name='product_list'),
    url('catalog/<str:category_slug>/', views.product_list, name='product_list_by_category'),
    url('product/<str:slug>/', views.product_detail, name='product_detail'),
    url('post/<str:slug>/', views.post_comment, name='post_comment'),
    url('', views.main_page, name='index'),
    url("signup/", views.SignUpView.as_view(), name="signup"),
    url("profile/", views.profile, name="profile"),
    url("edit-profile/", views.edit_profile, name="edit_profile"),
    url('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
    url('history/', views.history, name='history'),
    url('order/<int:order_id>/', views.order, name='order'),
]
