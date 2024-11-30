import json
import os
import hashlib
import requests
import time


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
def get_html_page(url: str, pause: float = 0) -> str:
   response = requests.get(url)
   if response.ok:
       if pause > 0: time.sleep(pause)
       return response.text
   else:
       raise Exception(f'Cannot retrieve {url}: status code = {response.status_code}, text = {response.text}')
