from django.urls import path
from .views import register_user, login, CreatePostView, delete_post, like_post, unlike_post, analytics, PostListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login, name='login'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('', PostListView.as_view(), name='post-list'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('unlike_post/<int:post_id>/', unlike_post, name='unlike_post'),
    path('analytics/', analytics, name='analytics'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
