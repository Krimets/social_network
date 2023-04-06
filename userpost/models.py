from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts')

    def __str__(self):
        return self.text


# добавляем параметр related_name для связей в модели User
User._meta.get_field('groups').related_name = 'auth_user_groups'
User._meta.get_field('user_permissions').related_name = 'auth_user_permissions'
