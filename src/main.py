import argparse
import configparser
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class Config:
    # Получаем настройки из файла ini
    __config = configparser.ConfigParser()
    if __config.read('src/config/settings.ini'):
        tags = __config.get('Webparser', 'tags', fallback='').split(',')
        div_classes = __config.get('Webparser', 'div_classes', fallback='').split(',')
    else:
        tags = []
        div_classes = []
    if div_classes:
        tags.append('div')


cfg = Config()


def get_url():
    # Получаем ссылку из аргументов
    parser = argparse.ArgumentParser(description='Webparser')
    parser.add_argument('--url', required=True, help='URL')
    args = parser.parse_args()
    return args.url


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


def get_text_with_links(elem, dom):
    # Получаем отформатированный текст с вставленными ссылками
    for link in elem.find_all('a'):
        link_text = link.text.strip()
        link_href = link["href"]
        if link_href.startswith('/'):
            link_href = dom + link_href
        link.replace_with(link_text + ' [' + link_href + ']')
    return split_into_lines(elem.text.strip())


def is_class_in_config(list_cls):
    # Проверяем, что полученные классы div содержится в настройках
    for cls in cfg.div_classes:
        if cls in list_cls:
            return True
    return False


def main():
    url = get_url()
    # Получаем html из указанной ссылки
    r = requests.get(url)
    html = r.text
    # Используем BeautifulSoup для парсинга html
    soup = BeautifulSoup(html, 'html.parser')

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
        if elem.name != 'div' or elem.name == 'div' and elem.has_attr('class') and is_class_in_config(elem['class']):
            elem_text = get_text_with_links(elem, dom)
            if len(elem_text) > 0:
                text += '\n\n' + elem_text

    # Сохраняем в файл
    file_name = (url_parse.netloc + url_parse.path + ".txt").replace('/', '_')
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(text)


if __name__ == '__main__':
    main()
