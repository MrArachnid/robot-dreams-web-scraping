import csv
import sqlite3
import xml.etree.ElementTree as ET

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

import requests
import hashlib
import os
import json
import re
from pprint import pprint
from typing import TypeAlias

StrPairList: TypeAlias = list[tuple[str, str]]

def file_cache(func):
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
def get_content(url: str) -> str|None:
    response = requests.get(url)
    return response.text if response.ok else None


@file_cache
def post_content(url: str, payload: dict) -> dict|None:
    response = requests.post(url, json=payload)
    return response.json() if response.ok else None


def scrape_job_cards(url: str) -> StrPairList:
    # first page
    content = get_content(url)
    job_cards = find_job_cards(content)

    # next pages
    for page_num in range(2, 4):
        payload = {"action":"facetwp_refresh","data":{"facets":{"recherche":[],"ou":[],"type_de_contrat":[],"fonction":[],"load_more":[page_num]},"frozen_facets":{"ou":"hard"},"http_params":{"get":[],"uri":"emplois","url_vars":[]},"template":"wp","extras":{"counts":True,"sort":"default"},"soft_refresh":1,"is_bfcache":1,"first_load":0,"paged":page_num}}
        content = post_content(url, payload)
        job_cards += find_job_cards(content['template'])

    return job_cards


def find_job_cards(content: str) -> StrPairList:
    cards = re.findall(r'<div class=" w-full ">(.*?)<footer', content, re.MULTILINE | re.DOTALL)
    return [
        (
            re.findall(r'<h3 class="jobCard_title m-0">(.*?)</h3>', card)[0],
            re.findall(r'<a href="(.*?)"', card)[0],
        )
        for card in cards
    ]


def save_cards_to_csv(cards: StrPairList) -> None:
    with open('job_cards.csv', mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(('title', 'url'))
        writer.writerows(cards)


def save_cards_to_json(cards: StrPairList) -> None:
    cards = [{ 'title': title, 'url': url} for title, url in cards]
    with open('job_cards.json', 'w', encoding='utf-8') as f:
        json.dump(cards, f, indent=4)


def save_cards_to_sqlite(cards: StrPairList) -> None:
    conn = sqlite3.connect('job_cards.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT    
            )''')
        for title, url in cards:
            cursor.execute(
                'INSERT INTO cards (title, url) values (?, ?)',
                (title, url)
            )
        conn.commit()
    finally:
        conn.close()


def save_cards_to_sqlalchemy(cards: StrPairList) -> None:
    filename = 'job_cards_sqlalchemy.db'
    engine = create_engine('sqlite:///' + filename)
    Base = declarative_base()

    class Card(Base):
        __tablename__ = 'cards'
        id = Column(Integer, primary_key=True)
        title = Column(String)
        url = Column(String)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        for title, url in cards:
            session.add(Card(
                title=title,
                url=url
            ))
        session.commit()
    finally:
        session.close()


def save_cards_to_xml(cards: StrPairList) -> None:
    root = ET.Element('cards')
    for title, url in cards:
        card_element = ET.SubElement(root, 'card')
        ET.SubElement(card_element, 'title').text = title
        ET.SubElement(card_element, 'url').text = url
    tree = ET.ElementTree(root)
    tree.write('job_cards.xml', encoding='utf-8', xml_declaration=True)


def main():
    url = 'https://www.lejobadequat.com/emplois'

    job_cards = scrape_job_cards(url)
    pprint(job_cards)

    save_cards_to_csv(job_cards)
    save_cards_to_json(job_cards)
    save_cards_to_sqlite(job_cards)
    save_cards_to_sqlalchemy(job_cards)
    save_cards_to_xml(job_cards)


if __name__ == '__main__':
    main()