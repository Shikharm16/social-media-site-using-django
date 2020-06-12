from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_view


from .views import (
    PostListView,
    # PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('', views.feed,name='socio-feed'),
    path('profile/', views.profile,name='socio-profile'),
    path('signup/', views.signup,name='socio-register'),
    path('', views.home, name='socio-home'),
    path('Newsfeed/', PostListView.as_view(), name='socio-feed'),
    path('trending/', views.trending, name='socio-trending'),
# path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),extra_context={'title':'Socio Newsfeed'}
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', PostCreateView.as_view(extra_context={'title':'New Post'}), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('logout/', auth_view.LogoutView.as_view(template_name='socio/logout.html'),name='logout'),
    path('deactivate/', views.delete_user, name='socio-delete'),
    path('likes/',views.postlike,name='socio-like'),
    path('dashboard/', views.dashboard, name='socio-dashboard'),
    path('comment/<int:id>', views.deletecomment, name='socio-comment'),
    path('filtered/', views.filter_list, name='socio-filter'),
    path('deactivate/confirm/', views.delete_user_confirm, name='socio-delete-confirm'),
    url(r'(?P<id>\d+)/saved/$',views.favorite,name='socio-favorite'),
    path('bookmark/', views.favorite_list, name='socio-bookmark'),
    path('docx/', views.document, name='socio-docx'),
]
