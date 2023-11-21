# Парсер веб-страницы

## Описание

Программа извлекает полезный текст из веб-страницы и сохраняет его в файл txt.
Программа оформлена в виде утилиты командной строки, которой в качестве параметра
указывается URL.

Пример запуска: python main.py --url https://lenta.ru/news/2013/03/dtp/index.html

В файле settings.ini задаются теги искомых элементов и классы, для элементов div.

## Библиотеки

argparse, configparser, urlparse, requests, BeautifulSoup

## Результаты

Список URL на которых проходило тестирование:
- https://ria.ru/20231120/zagrazhdeniya-1910643784.html
- https://lenta.ru/news/2023/11/21/belyy-dom-otvetil-na-vopros-ob-otkaze-ot-tehnologiy-spacex-posle-zayavleniy-maska/
- https://www.gazeta.ru/business/news/2023/11/20/21751711.shtml

Результаты находятся в папке examples.

## Дальнейшее улучшение

- Расширить возможность настройки для нахождения полезного текста.
- Добавить настройки форматирования текста для выходного файла.