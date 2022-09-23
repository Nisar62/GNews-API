"""gnews URL Configuration

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
from django.urls import path, include
from gnews import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	path("admin/", admin.site.urls),
    path('auth/', include('auth.urls')),
	path('', views.main_page, name="main_page"),
	path('login/', views.login, name="login"),
	path('logout/', views.logout, name="logout"),
	path('home/', views.home, name="home"),
	path('login/response', views.login_response, name="login_response"),
	path('register/', views.register, name="register"),
	path('register/response', views.register_response, name="register_response"),
	path('top_records/', views.get_top_records, name="get_top_records"),
	path('top_records/response', views.top_records_response, name="top_records_response"),
	path('search_records/', views.search_records, name="search_records"),
	path('search_records/response', views.search_records_response, name="search_records_response"),
]