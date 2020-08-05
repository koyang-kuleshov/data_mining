from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Settings

from habr_parse import settings
from habr_parse.spiders.habr_posts import HabrPostsSpider, AuthorInfoSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_proc = CrawlerProcess(settings=crawler_settings)

    crawler_proc.crawl(HabrPostsSpider)

    crawler_proc.start()
