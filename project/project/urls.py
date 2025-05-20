"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.hello,name='index'),
    path('login/',views.logi,name='login'),
    path('register/',views.register1,name='register'),
    path('user/',views.complaintsub,name='user'),
    
    path('profile/',views.updateprofile,name='profile'),
    path('profileg/',views.updateprofileg,name='profileg'),
    
    path('login_redirect/', views.login_redirect, name='login_redirect'),
    path('logout/', views.logout_view, name='logout'),
    path('solved/', views.solvedlist, name='solved'),
    path('alllist/', views.alllist, name='alllist'),
    
    path('passwordchange/', views.passwordchange, name='passwordchange'),
    path('passwordchangeg/', views.passwordchangeg, name='passwordchangeg'),
    
    path('counter/', views.counter, name='counter'),
    path('allcomplaints/', views.allcomplaints, name='allcomplaints'),
    path('solvedcomplaints/', views.solvedcomplaints, name='solvedcomplaints'),
    path('complaint/<int:complaint_id>/pdf/', views.generate_complaint_pdf, name='generate_complaint_pdf'),
]
