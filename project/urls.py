"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from views import login_view, register_view, logout_view, dashboard_view, task_detail_view, comment_create_view, profile_view

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API
    path('api/', include('users.urls')),
    path('api/', include('classes.urls')),
    path('api/', include('tasks.urls')),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),

    # Templates/Web
    path('', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('tasks/<int:task_id>/', task_detail_view, name='task_detail'),
    path('comments/create/', comment_create_view, name='comment_create'),
]
