from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Homepage & Search
    path('', views.index_view, name='index'),

    # Filters
    path('category/<slug:slug>/', views.category_posts_view, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts_view, name='tag_posts'),

    # Custom Premium Site Admin Panel
    path('site-admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('site-admin/user/<int:pk>/toggle-author/', views.admin_user_toggle_author_view, name='admin_user_toggle_author'),
    path('site-admin/post/<slug:slug>/toggle-status/', views.admin_post_toggle_status_view, name='admin_post_toggle_status'),
    path('site-admin/category/create/', views.admin_category_create_view, name='admin_category_create'),
    path('site-admin/category/<int:pk>/edit/', views.admin_category_edit_view, name='admin_category_edit'),
    path('site-admin/category/<int:pk>/delete/', views.admin_category_delete_view, name='admin_category_delete'),
    path('site-admin/tag/create/', views.admin_tag_create_view, name='admin_tag_create'),
    path('site-admin/tag/<int:pk>/delete/', views.admin_tag_delete_view, name='admin_tag_delete'),

    # Author Dashboard & Post CRUD
    path('dashboard/', views.author_dashboard_view, name='author_dashboard'),
    path('post/create/', views.post_create_view, name='post_create'),
    path('post/<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),

    # Post Detail & Actions
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/like/', views.like_toggle_view, name='like_toggle'),
    path('post/<slug:slug>/comment/', views.comment_create_view, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),

    # Author Profile
    path('author/<str:username>/', views.author_profile_view, name='author_profile'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
