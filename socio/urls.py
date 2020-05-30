from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_view


from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('', views.feed,name='socio-feed'),
    path('profile', views.profile,name='socio-profile'),
    path('signup', views.signup,name='socio-register'),
    path('', views.home, name='socio-home'),
    path('feed/', PostListView.as_view(), name='socio-feed'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('logout/', auth_view.LogoutView.as_view(template_name='socio/logout.html'),name='logout'),
    path('deactivate/', views.delete_user, name='socio-delete'),
    path('filtered/', views.filter_list, name='socio-filter'),
    path('deactivate/confirm', views.delete_user_confirm, name='socio-delete-confirm'),
]
