from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.post_search, name='post_search'),
    path('<slug:slug>/', views.post_single, name='post_single'),
    path('category/<category>/', views.CategoryListView.as_view(), name='category'),
]
