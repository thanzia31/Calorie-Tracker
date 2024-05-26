"""calorie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from calorieApp import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.Register),
    path('',views.index),
    path("userdetail/",views.UserDetailView),
    path('accounts/login/index1/',views.index1),
    path("accounts/",include('django.contrib.auth.urls')),
    path("additem/",views.AddItemView),
    path("deleteitem/<int:id>/",views.delete_item),
    path("updateitem/<int:id>/",views.update_item),
    path("profile/",views.profile),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='calorieApp/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='calorieApp/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='calorieApp/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='calorieApp/password_reset_complete.html'),name='password_reset_complete'),
    path('trackrecord/',views.trackrecord),
    path('visualize/',views.visualize),
    path('verifyotp/',views.verify_otp,name='verifyotp'),
    path('get_food_item/', views.get_food_item, name='get_food_item'),
    path('recc_item/',views.recc_item),
    path('get_recepie/',views.get_recepie,name='get_recepie')
]
    
