from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, AnalyticsSerializer, CreatePostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post
from django.views.generic import ListView
from django.db import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.http import JsonResponse


@login_required
def user_like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes.add(request.user)
    post.save()
    likes_count = post.likes.count()
    return JsonResponse({'likes_count': likes_count})


@login_required
def user_unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes.remove(request.user)
    post.save()
    likes_count = post.likes.count()
    return JsonResponse({'likes_count': likes_count})


def user_logout(request):
    logout(request)
    return redirect('post-list')


@login_required
def user_create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post-list')
    else:
        form = PostForm()
    return render(request, 'userpost/create_post.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('post-list')
    else:
        form = AuthenticationForm()
    return render(request, 'userpost/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = UserCreationForm()
    return render(request, 'userpost/register.html', {'form': form})


class PostListView(ListView):
    model = Post
    template_name = 'userpost/post_list.html'
    context_object_name = 'posts'


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if not post:
        return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    post.likes.add(request.user)
    return Response({'detail': 'Post liked successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if not post:
        return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    post.likes.remove(request.user)
    return Response({'detail': 'Post unliked successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics(request):
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')

    if not date_from or not date_to:
        return Response({'detail': 'Both "date_from" and "date_to" query parameters are required'}, status=status.HTTP_400_BAD_REQUEST)

    likes_count = Post.objects.filter(created_at__range=[date_from, date_to]).values('created_at').annotate(likes_count=models.Count('likes'))

    serializer = AnalyticsSerializer({'likes_by_date': likes_count})
    return Response(serializer.data, status=status.HTTP_200_OK)

