from django.shortcuts import render
from .models import Article
from .serializers import ArticleSerializer

from rest_framework import generics

# Create your views here.

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.select_related('source').all()
    serializer_class = ArticleSerializer
    filterset_fields = ['status', 'source']
    search_fields = ['title', 'content']


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.select_related('source').all()
    serializer_class = ArticleSerializer