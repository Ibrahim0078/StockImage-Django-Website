"""
URL configuration for pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('',views.main,name = 'main'),
    path('accounts/login/',views.user_login,name = 'login'),
    path('signup/',views.signup,name = 'signup'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('aboutus/',views.aboutus,name = 'aboutus'),
    path('contactus/',views.contactus,name = 'contactus'),
    path('download_image/<int:image_id>/', views.download_image, name='download_image'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('logout/',views.user_logout,name = 'logout'),
    path('upload/', views.upload_image, name='upload_image'),
    path('activate/<str:id>/',views.activate,name = 'activate'),
    path('reset', PasswordResetView.as_view(), name='reset_password'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
