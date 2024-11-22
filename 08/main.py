from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
from pprint import pprint

MAX_PAGES = 2

def parse():
    driver = webdriver.Chrome()

    try:
        result = []
        wait = WebDriverWait(driver, 10)
        for page in range(1, MAX_PAGES + 1):
            driver.get(f'https://jobs.marksandspencer.com/job-search?page={page}&query=&places_position=&places_name=')
            cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="ais-Hits-item"]')))
            for card in cards:
                result.append({
                    'title': card.find_element(By.TAG_NAME, 'h3').text,
                    'url': card.find_element(By.TAG_NAME, 'a').get_attribute('href')

                })

        return result
    finally:
        driver.quit()


def save_jobs_to_sqlite(jobs: list[dict]) -> None:
    conn = sqlite3.connect('marksandspencer_jobs.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT    
            )''')
        for job in jobs:
            cursor.execute(
                'INSERT INTO jobs (title, url) values (?, ?)',
                (job['title'], job['url'])
            )
        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    jobs = parse()
    save_jobs_to_sqlite(jobs)
    pprint(jobs)