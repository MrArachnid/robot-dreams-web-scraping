import requests
import hashlib
import os
import json
import inspect
import re
from pprint import pprint


def file_cache(func):
    """
    Декоратор для кешування у файл виклику
    будь-якої функції з будь-яким набором аргументів
    """
    def wrapper(*args, **kwargs):
        cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        cache_key_data = json.dumps([
            inspect.currentframe().f_code.co_name,
            args, kwargs
        ], sort_keys=True)
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
    return response.text if response.status_code == 200 else None


@file_cache
def post_content(url: str, payload: dict) -> dict|None:
    response = requests.post(url, json=payload)
    return response.json() if response.status_code == 200 else None


def find_job_cards(content: str) -> list:
    cards = re.findall(r'<div class=" w-full ">(.*?)<footer', content, re.MULTILINE | re.DOTALL)
    return [
        {
            'title': re.findall(r'<h3 class="jobCard_title m-0">(.*?)</h3>', card)[0],
            'url': re.findall(r'<a href="(.*?)"', card)[0],
        }
        for card in cards
    ]


def main():
    url = 'https://www.lejobadequat.com/emplois'

    # get
    content = get_content(url)
    pprint(find_job_cards(content))

    # post
    payload = {"action":"facetwp_refresh","data":{"facets":{"recherche":[],"ou":[],"type_de_contrat":[],"fonction":[],"load_more":[2]},"frozen_facets":{"ou":"hard"},"http_params":{"get":[],"uri":"emplois","url_vars":[]},"template":"wp","extras":{"counts":True,"sort":"default"},"soft_refresh":1,"is_bfcache":1,"first_load":0,"paged":2}}
    content = post_content(url, payload)
    pprint(find_job_cards(content['template']))


if __name__ == '__main__':
    main()