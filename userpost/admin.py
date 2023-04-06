from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('text', 'user__username')



