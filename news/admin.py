from django.contrib import admin
from .models import Source, Article

# Register your models here.
@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'source_type', 'is_active', 'last_scraped_at']
    list_filter = ['source_type', 'is_active']
    search_fields = ['name', 'url']
    readonly_fields = ['last_scraped_at', 'created_at', 'updated_at']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'status', 'published_at']
    list_filter = ['status', 'source']
    search_fields = ['title', 'content']
    readonly_fields = ['scraped_at', 'created_at', 'updated_at']