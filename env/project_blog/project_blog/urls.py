"""
URL configuration for project_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from blog import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='blog-home'),
    path('post-form/', views.post_form, name='blog-post-form'), 
    path('post/<int:post_id>/delete/', views.delete_post, name='delete-post'),
    path('post/<slug:slug>/', views.post_details, name='post_details'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit-post'),
    
    path('categories/', views.category_list, name='category-list'),
    path('categories/create/', views.category_create, name='create-category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit-category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete-category'),
    
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
