import logging
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from os import path
import argparse
from urllib.parse import urljoin
import json


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Генератор страницы сайта библиотеки www.tululu.org"
    )
    parser.add_argument(
        '--dest_folder',
        default='General',
        type=str,
        help='Путь к каталогу с данными для генерации',
    )
    args = parser.parse_args()
    return args


def find_json_files(directory):
    json_files = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            json_files.append(file)
    return json_files


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d - %(levelname)-8s - %(message)s'
    )

    logger = logging.getLogger(__name__)
    base_dir = path.dirname(path.abspath(__file__))
    parsed_arguments = parse_arguments()
    general_folder = parsed_arguments.dest_folder
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    data_structures_file = find_json_files(general_folder)[0]
    with open(os.path.join(general_folder, data_structures_file), "r") as json_file:
        book_details = json_file.read()
    books = json.loads(book_details)

    for item_book_path in books:
        item_book_path['img_path'] = urljoin(general_folder+'/', str(item_book_path['img_path']))

    rendered_page = template.render(books=books)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)