from rest_framework import serializers
from .models import Source, Article


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['id', 'name', 'url', 'source_type']

class ArticleSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'url', 'content', 'author', 'source', 'status', 'published_at', 'created_at',
        ]