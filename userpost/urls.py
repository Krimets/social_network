from django.urls import path
from .views import register_user, login, CreatePostView, like_post, unlike_post, analytics, PostListView, register, \
    user_login, user_create_post, user_logout
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),

    path('register/', register, name='user-register'),
    path('login/', user_login, name='user-login'),
    path('create_post/', user_create_post, name='user-create_post'),
    path('logout/', user_logout, name='user-logout'),

    path('api/register/', register_user, name='register'),
    path('api/login/', login, name='login'),
    path('api/create_post/', CreatePostView.as_view(), name='create_post'),
    path('api/like_post/<int:post_id>/', like_post, name='like_post'),
    path('api/unlike_post/<int:post_id>/', unlike_post, name='unlike_post'),
    path('api/analytics/', analytics, name='analytics'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
