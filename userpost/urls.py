from django.urls import path
from .views import register_user, login, CreatePostView, like_post, unlike_post, analytics, PostListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/register/', register_user, name='register'),
    path('api/login/', login, name='login'),
    path('api/create_post/', CreatePostView.as_view(), name='create_post'),
    path('', PostListView.as_view(), name='post-list'),
    path('api/like_post/<int:post_id>/', like_post, name='like_post'),
    path('api/unlike_post/<int:post_id>/', unlike_post, name='unlike_post'),
    path('api/analytics/', analytics, name='analytics'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
