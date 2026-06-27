from django.db import models
from django.utils import timezone
from datetime import timedelta


class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')
    
    def draft(self):
        return self.filter(status='draft')
    
    def recent(self, days=7):
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(published_at__gte=cutoff)
    
    def by_source(self, source):
        return self.filter(source=source)
    
    def active_sources(self):
        return self.filter(source__is_active=True)
    
