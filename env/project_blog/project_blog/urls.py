from django.contrib import admin
from django.urls import path
from blog import views
from django.views.i18n import set_language
from django.conf.urls.i18n import i18n_patterns


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
    
    path('posts/category/<int:category_id>/', views.category_page, name='category_pages'),
    path('posts/', views.category_page, name='all_posts'),
    
    path('post/<int:post_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('user/favorites/', views.user_favorites, name='user_favorites'),
    
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += i18n_patterns(
    path('set_language/', set_language, name='set_language'),
)
