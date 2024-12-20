import os
import hashlib
import json
import pprint
import sqlite3

from bs4 import BeautifulSoup
import requests


def file_cache(func: callable) -> callable:
    """
    Декоратор для кешування у файл виклику
    будь-якої функції з будь-яким набором аргументів
    """
    def wrapper(*args, **kwargs):
        cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        cache_key_data = json.dumps([func.__name__, args, kwargs], sort_keys=True)
        filename = os.path.join(
            cache_dir,
            hashlib.md5(cache_key_data.encode('utf-8')).hexdigest()
        )
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)

        result = func(*args, **kwargs)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f)
        return result
    return wrapper


@file_cache
def get_html_content(url: str) -> str:
    response = requests.get(url)
    return response.text if response.ok else None


def parse_front_page(url: str) -> list[dict]:
    html = get_html_content(url)
    soup = BeautifulSoup(html, 'lxml')

    articles = soup.find_all('div', {'type': 'article'})
    return [
        {
            'Link': (article_url := 'https://www.bbc.com' + article.find('a').get('href')),
            'Topics': parse_article_page(article_url)
        }
        for article in articles[:5]
    ]


def parse_article_page(url: str) -> list[str]:
    html = get_html_content(url)
    soup = BeautifulSoup(html, 'lxml')
    topic_list = (soup
                  .find('div', {'data-component': 'topic-list'})
                  .find('ul', {'role': 'list'}))
    return [topic.text for topic in topic_list.find_all('li')]


def save_articles_to_sqlite(articles: list[dict]) -> None:
    conn = sqlite3.connect('bbc_sport_articles.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT,
                topics TEXT    
            )''')
        for article in articles:
            cursor.execute(
                'INSERT INTO articles (link, topics) values (?, ?)',
                (article['Link'], ', '.join(article['Topics']))
            )
        conn.commit()
    finally:
        conn.close()


def main():
    url = 'https://www.bbc.com/sport'
    articles = parse_front_page(url)
    pprint.pprint(articles)
    save_articles_to_sqlite(articles)

if __name__ == '__main__':
    main()