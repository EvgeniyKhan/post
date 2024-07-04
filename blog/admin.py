from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview', 'count_view', 'created_at')
    search_fields = ('title', 'created_at')
