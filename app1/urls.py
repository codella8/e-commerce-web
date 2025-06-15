from django.urls import path
from . import views
from .views import admin_panel

urlpatterns = [
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name ='signup'),
    path('accounts/login/', views.login_user, name='login'),
    path('update_user/', views.update_user, name ='update_user'),
    path('update_info/', views.update_info, name ='update_info'),
    path('update_password/', views.update_password, name ='update_password'),
    path('category/<slug:cat>/', views.category, name='category'),
    path('product/<int:pk>/', views.product, name ='product'),
    path('additionalproduct/', views.additionalproduct, name='additionalproduct'),
    path('additionalproduct/<int:id>/', views.additionalproduct_detail, name='additionalproduct_detail'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('orders/', views.user_orders, name='orders'),
    path('order_details/<int:pk>/', views.order_details, name='order_details'),
] 