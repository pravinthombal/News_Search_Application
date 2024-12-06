# urls.py
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('search/', views.search_news, name='search_news'),  # Search news page
    path('history/', views.search_history, name='search_history'),  # Search history page
    path('results/<int:search_query_id>/', views.view_results, name='view_results'),  # View specific search results
    path('refresh/<int:search_query_id>/', views.refresh_search, name='refresh_search'),  # Refresh search results
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='search_history'), name='logout'),  # Logout path
]
