# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'info_manage'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('food_detail/<int:food_id>/', views.food_detail, name='food_detail'),
    path('food_list/<int:category_id>/', views.food_list, name='food_list'),
    path('add_like/', views.add_like, name='add_like'),
    path('my_like/', views.my_like, name='my_like'),
    path('my_order/', views.my_order, name='my_order'),
    path('my_info/', views.my_info, name='my_info'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('view_count/', views.view_count, name='view_count'),
    path('input_score/', views.input_score, name='input_score'),
    path('check_page/', views.check_page, name='check_page'),
    path('img_upload/', views.img_upload, name='img_upload'),
    path('food_check/', views.food_check, name='food_check'),
    path('item_recommend/<int:user_id>/', views.user_based_recommendation, name='item_recommend'),
]
