from bs4 import BeautifulSoup
import requests
from datetime import datetime
from urllib.parse import urljoin, urlparse
from dCore.dstring import Dstring
import re
import json

from dgSql.dmysql import Dmysql


class BaseCrawler:
    def parse_datetime(self, datestring: str):
        return datetime.strptime(datestring, '%m/%d/%Y %H:%M:%S %p')

    def parse_category(self, category: dict):
        link = category['link']
        title = category['title']
        category['slug'] = Dstring.slug(title, delim='-')
        category['id'] = int(re.search(r'c(\d+)\.htm', urlparse(link).path.split('/')[-1]).group(1))
        return category

    def parse_article(self, article):
        link = article['link']
        article['id'] = re.search(r'd(\d+)\.htm', link.split('/')[-1]).group(1)
        return article


class CrawlerBaoNinhBinh(BaseCrawler):
    MAX_PAGE = 10000
    mysql = {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': '123456',
        'db': 'baoninhbinh'
    }
    SMY = Dmysql(host=mysql['host'], user=mysql['user'], passwd=mysql['passwd'], db=mysql['db'], keep_connect=True)
    BASE_URL = 'https://baoninhbinh.org.vn/'
    RQ_SESSION = requests.Session()
    RQ_SESSION.headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    }

    def __init__(self):
        pass

    def get_list_category(self):
        rq = self.RQ_SESSION.get(self.BASE_URL)
        if rq:
            html = rq.content.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            footer = soup.find('footer', id='footer')
            categorys = []
            for a_tag in footer.find_all('a'):
                categorys.append(self.parse_category({'link': a_tag.get('href'), 'title': a_tag.text.strip()}))
            return categorys

    def get_list_article(self, category: dict, page=1):
        if page > self.MAX_PAGE:
            return
        link = category['link']
        rq = self.RQ_SESSION.get(link)
        if rq:
            html = rq.content.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            list_by_cat = soup.find('div', class_='list-by-cat')
            for item in list_by_cat.find_all('div', class_='item'):
                article = {
                    'category_id': category['id']
                }
                a_tag = item.find('a')
                img_tag = item.find('img')
                article['link'] = a_tag.get('href')
                article['title'] = a_tag.get('title')
                article['thump'] = img_tag.get('src')
                article['description'] = item.find('p', class_='item-des').text.strip()
                yield article
            paging = soup.find('ul', class_='pagination')
            if paging:
                next_li = paging.find('li', class_='next')
                if next_li:
                    next_url = next_li.find('a').get('href')
                    category['link'] = urljoin(link, next_url)
                    for article in self.get_list_article(category, page=page + 1):
                        yield article

    def check_exist_article(self, article):
        article_from_db = self.SMY.query_row('SELECT id FROM article WHERE  id=:id LIMIT 1', {'id': article['id']})
        if article_from_db:
            return True
        return False

    def get_detail_article(self, article: dict):
        article = self.parse_article(article)
        link = article['link']
        if self.check_exist_article(article):
            print(link, 'Exists')
            return

        print(link)
        rq = self.RQ_SESSION.get(link)
        if rq:
            html = rq.content.decode('utf-8')
            soup = BeautifulSoup(html, 'lxml')
            article['keywords'] = soup.find('meta', {'name': 'keywords'}).get('content')
            article['publish'] = self.parse_datetime(soup.find('div', class_='post-meta-date').get('content'))
            entry_media = soup.find('div', class_='entry-media')
            if entry_media and entry_media.find('img'):
                article['media'] = {'src': entry_media.find('img').get('src'), 'caption': entry_media.find('p', class_='image-caption').text.strip()}
                article['media'] = json.dumps(article['media'])
            article['content'] = soup.find('div', class_='entry-content').decode_contents(formatter='html').strip()
            del article['link']
            article['keywords'] = article['keywords']
            article['slug'] = Dstring.slug(article['title'], delim='-')
            print(article)
            print(article['id'], article['title'], self.SMY.insert('article', article))

    def upsert_category(self, category):
        category_from_db = self.SMY.query_row('SELECT id FROM category WHERE id=:id', {'id': category['id']})
        if not category_from_db:
            category['locked'] = 0
            del category['link']
            print(category)
            self.SMY.insert('category', category)

    def run(self):
        for category in self.get_list_category():
            print(category)
            self.upsert_category(category)
            for article in self.get_list_article(category):
                self.get_detail_article(article)


if __name__ == '__main__':
    CrawlerBaoNinhBinh().run()
