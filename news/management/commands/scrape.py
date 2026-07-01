import requests 
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Source, Article


class Command(BaseCommand):
    help = "Scrape articles from all active sources"

    def handle(self, *args, **options):
        sources = Source.objects.filter(is_active=True)

        if not sources.exists():
            self.stdout.write(self.style.WARNING("No active sources found."))
            return
        
        for source in sources:
            self.stdout.write(f"Scrapping:{source.name}...")
            self.scrape_sources(source)

    def scrape_sources(self, source):
        try:
            response = requests.get(source.url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f" Failed to fetch {source.url}: {e}"))
            return
        
        soup = BeautifulSoup(response.text,'html.parser')
        articles = self.parse_articles(soup, source)

        self.stdout.write(f" Found {len(articles)} new articles")
        # self.stdout.write(f" Fetched {source.url} successfully")

        source.last_scraped_at = timezone.now()
        source.save(update_fields=['last_scraped_at'])

    def parse_articles(self, soup, source):
        created = []

        for link in soup.find_all('a',href=True):
            href = link['href']
            title = link.get_text(strip=True)

            if '/news/' not in href or not title:
                continue
            # skip news categories/sections
            if not href.rstrip('/').split('-')[-1].isdigit():
                continue

            #Build full URL if relative
            if href.startswith('/'):
                article_url = source.url.rstrip('/') + href
            else:
                article_url = href

            #skip if we already have this article
            if Article.objects.filter(url=article_url).exists():
                continue
            
            article = Article.objects.create(
                source=source,
                title=title,
                url= article_url,
                status='draft',
                scraped_at=timezone.now(),
            )
            created.append(article)
        
        return created