from django.db import models

# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    source_type = models.CharField(
        max_length=10,
        choices=[
            ('rss', 'RSS Feed'),
            ('html', 'HTML Scraping'),
            ('api', 'API'),
        ],
        default='html',
    )
    scrape_config = models.JSONField(
        default=dict,
        blank=True,
        help_text= "CSS selectors and patterns for scraping this source",
    )
    is_active = models.BooleanField(default=True)
    scrape_interval = models.PositiveIntegerField(
        default=60,
        help_text="Minutes between scrape attempts",
    )
    last_scraped_at =models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering =['name']

class Article(models.Model):
    source = models.ForeignKey(
        Source,
        on_delete=models.PROTECT,
        related_name='articles',
    )
    title = models.CharField(max_length=500)
    url = models.URLField(unique=True)
    content = models.TextField(blank=True,default="")
    author = models.CharField(max_length=255, blank=True, default="")
    published_at = models.DateTimeField(null=True, blank=True)
    scraped_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('archived', 'Archived'),
        ],
        default='draft',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_at']
