from scrapy.crawler import CrawlerProcess
from filmscraper.spiders.imdb_spider import ImdbSpider
import asyncio
import time
import aiosqlite

DB_FILE = "movies_cache.db"

custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/116.0.0.0 Safari/537.36',
    'ROBOTSTXT_OBEY': False,
}

async def save_movie(movie_id, title, imdb_rating, timestamp):
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute(
            "INSERT OR REPLACE INTO movies (movie_id, title, imdb_rating, timestamp) VALUES (?, ?, ?, ?)",
            (movie_id, title, imdb_rating, timestamp)
        )
        await db.commit()

class SavePipeline:
    def process_item(self, item, spider):
        asyncio.run(save_movie(
            item['movie_id'],
            item['title'],
            item['imdb_rating'],
            int(time.time())
        ))
        return item

def run_spider(movie_id):
    process = CrawlerProcess({
    'ITEM_PIPELINES': {'__main__.SavePipeline': 300},
    'LOG_LEVEL': 'DEBUG',
    })
    process.crawl(ImdbSpider, movie_id=movie_id)
    process.start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python run_spider.py <movie_id>")
        exit(1)
    run_spider(sys.argv[1])
