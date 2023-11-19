import argparse
import configparser
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def get_url():
    # Получаем ссылку из аргументов
    parser = argparse.ArgumentParser(description='Webparser')
    parser.add_argument('--url', required=True, help='URL')
    args = parser.parse_args()
    return args.url


class Config:
    # Получаем настройки изи файла ini
    __config = configparser.ConfigParser()
    __config.read('settings.ini')
    tags = __config['Webparser']['tags'].split(',')


url = get_url()
cfg = Config


def split_into_lines(text):
    # Форматируем текст: ширина строк не больше 80
    result = ''
    words = text.split()
    len_line = 0
    for word in words:
        len_word = len(word)
        if len_line == 0:
            result += word
            len_line = len_word
        elif len_line + len_word + 1 <= 80:
            result += ' ' + word
            len_line += len_word + 1
        else:
            result += '\n' + word
            len_line = len_word
    return result


def main():
    # Получаем html из указанной ссылки
    r = requests.get(url)
    html = r.text
    # Используем BeautifulSoup для парсинга html
    soup = BeautifulSoup(html, 'lxml')

    # Записываем заголовок
    title = soup.title
    if title:
        text = split_into_lines('Заголовок: ' + title.text.strip())
    else:
        text = '----------'

    # Получаем домен для записи неполных ссылок
    url_parse = urlparse(url)
    dom = url_parse.scheme + '://' + url_parse.netloc

    # Получаем теги указанные в настройках
    # Пробегаем по ним получая текстовое содержимое
    elem_all = soup.find_all(cfg.tags)
    for elem in elem_all:
        if elem.name.startswith('h'):
            text += '\n\n' + split_into_lines(elem.text.strip())
        else:
            for link in elem.find_all('a'):
                link_text = link.text.strip()
                link_href = link["href"]
                if link_href.startswith('/'):
                    link_href = dom + link_href
                link.replace_with(link_text + ' [' + link_href + ']')
            elem_text = split_into_lines(elem.text.strip())
            if len(elem_text) > 0:
                text += '\n\n' + elem_text

    # Сохраняем в файл
    file_name = (url_parse.netloc + url_parse.path + ".txt").replace('/', '_')
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(text)


if __name__ == '__main__':
    main()
