from django.urls import path,include
from .views import *
from. import views

urlpatterns = [
    path('',views.home, name='home'),
    path('blog/',views.blog, name='blog'),
    path('contact/',views.contact, name='contact'),
    path('post/<id>/',views.post, name='post-detail'),
    path('tinymce/',include('tinymce.urls')),
    path('post/<id>/update/', views.post_update, name = 'post-update'),
    path('post/<id>/delete/', views.post_delete, name = 'post-delete'),
    path('create/', views.post_create, name = 'post-create'),
    path('search/',views.search, name='search'),
    path('categories/<slug>/', views.category_detail, name='category-detail'),
    path('categories/', views.category, name="category")

]
