from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Settings

from avito_realestate import settings
from avito_realestate.spiders.avito_yel import AvitoYelSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    crawler_proc = CrawlerProcess(settings=crawler_settings)

    crawler_proc.crawl(AvitoYelSpider)

    crawler_proc.start()
