from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('error/', views.error, name='error'),
    path('', views.index, name='index'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('customer_list/<int:pk>/detail/', views.customer_detail, name='customer_detail'),
    path('massage_list/<int:pk>/detail/', views.massage_detail, name='massage_detail'),
    path('massage_list/<int:customer_pk>/add/', views.massage_add, name='massage_add'),
    path('customer/add/', views.customer_add, name='customer_add'),
]