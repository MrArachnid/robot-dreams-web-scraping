import json
from dataclasses import asdict

from utils import get_html_page
from schemas import Course
from bs4 import BeautifulSoup
from pprint import pprint

DELAY_BETWEEN_REQUESTS = 2
BASE_URL = 'https://robotdreams.cc'


def get_courses() -> list[Course]:
    result = []
    course_list_url = BASE_URL + '/uk/course'
    while course_list_url:
        html = get_html_page(course_list_url, DELAY_BETWEEN_REQUESTS)
        doc = BeautifulSoup(html, 'lxml')

        # отримуємо картки курсів
        cards = (doc
                 .find('ul', {'class': 'courses-list'})
                 .find_all('li', {'class': 'courses-list__item'}))
        for card in cards:
            course = parse_course_card(card)
            result.append(course)

        # шукаємо url наступної сторінки
        next_page = doc.find('li', {'class': 'page__item-next'})
        course_list_url = (BASE_URL + next_page.find('a')['href']) if next_page else None

    return result


def parse_course_card(card: BeautifulSoup) -> Course:
    course_url = BASE_URL + card.find('a')['href']

    course = Course(url=course_url)
    course.name = card.find('span', {'class': 'md-title'}).text
    course.short_descr = card.find('div', {'class': 'course-card__descr'}).text.strip()

    course.lector_name = card.find('p', {'class': 'course-card__lector-name'}).text.strip()
    course.lector_pos = card.find('p', {'class': 'course-card__lector-position'}).text.strip()
    lector_img = card.find('div', {'class': 'course-card__lector-img'}).find('img')
    course.lector_img = lector_img.attrs['data-src'] if lector_img else None

    parse_course(course)

    return course


def parse_course(course: Course) -> None:
    """
    Парсить сторінку курсу
    """
    html = get_html_page(course.url, DELAY_BETWEEN_REQUESTS)
    doc = BeautifulSoup(html, 'lxml')

    # full description
    full_descr = doc.find('div', {'class': ('about-course__description', 'info__desc')}) or \
                 doc.find('p', {'class': 'hero__description'})
    course.full_descr = full_descr.text.strip() if full_descr else course.short_descr

    # program
    program = doc.find('section', {'id': ('programm', 'program')}) or []
    if program:
        program_items = program.find_all('p', {'class': 'prog-item__lead'}) or\
                        program.find_all('p', {'class': 'text__vin--20'}) or \
                        program.find_all('span', {'class': 'program-item__name'}) or\
                        []
        for program_item in program_items:
            course.program.append(program_item.text.strip())


def save_to_json(courses: list[Course]) -> None:
    data = [asdict(course) for course in courses]
    with open('courses.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    courses = get_courses()
    save_to_json(courses)
    pprint(courses)
    print(f'Всього {len(courses)} курсів')


if __name__ == '__main__':
    main()
