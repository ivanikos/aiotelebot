# -*- coding: utf8 -*-
import requests
import random
from bs4 import BeautifulSoup


def get_weather(city):
    res = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=896831eabcb093f'
        f'c849059be7ffbff60&lang=ru')
    data = res.json()
    return data


def news():
    news = ''
    url = 'https://news.mail.ru/tag/226/'
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'lxml')
    res = soup.find('ul', class_='list list_type_square list_half js-module').find_all('a', class_='list__text')
    for item in res:
        news += f"{item.text} \n\n {str(item.get('href'))} \n\n "
    return news


def horo(sign):
    url = f'https://horo.mail.ru/prediction/{sign}/today/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    res = soup.find('div', class_='article__item article__item_alignment_left article__item_html').find_all('p')
    ans = res[0].text
    return ans


def exchange():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    ans = requests.get(url).json()
    return ans


"""
Чтение цитат из файла и возврат случайной цитаты.
"""


def quote_lao():
    with open('quote_lao.txt', 'r', encoding='cp1251') as f:
        lenta = f.read().splitlines()
    quotes = [x for x in lenta if x]
    return quotes[random.randint(1, 289)]


def quote_all():
    with open('quotes_all.txt', 'r', encoding='cp1251') as f:
        lenta = f.read().split(';')
    return lenta[random.randint(1, 675)]


def quote_budda():
    with open('quotes_budda.txt', 'r', encoding='cp1251') as f:
        lenta = f.read().split(';')
    return lenta[random.randint(1, 210)]


def english_words(word):
    url_page = f'https://www.translate.ru/%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4/' \
               f'%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9-%D1%80%D1%8' \
               f'3%D1%81%D1%81%D0%BA%D0%B8%D0%B9' \
               f'/{word}'

    res = requests.get(url_page)
    soup = BeautifulSoup(res.text, 'lxml')
    eng_word = soup.find('span', attrs={'class': 'source_only sayWord'})
    transcription = soup.find('span', attrs={'class': 'transcription'})
    part_speech = soup.find('span', attrs={'class': 'ref_psp'})

    translations = soup.find_all('div', attrs={'class': 'translation-item'})

    complete_string = f'{eng_word.text.upper()} \n {transcription.text.strip()} \n {part_speech.text} \n\n'
    for i in translations:
        try:
            translate = i.find('span', attrs={'class': 'result_only sayWord'})  # перевод
            try:
                ref_info = i.find('span', attrs={'class': 'ref_info'})  # род
            except:
                ref_info = ''
            eng_ex = i.find('div', attrs={'class': 'samSource'})  # пример 1 использования
            ru_ex = i.find('div', attrs={'class': 'samTranslation'})  # пример рус использования

            if not ref_info:
                complete_string = complete_string + f'{translate.text.upper()} \n\n ' \
                                                    f'{eng_ex.text} \n {ru_ex.text}\n\n'
            else:
                complete_string = complete_string + f'{translate.text.upper()} ({ref_info.text}) \n\n ' \
                                                    f'{eng_ex.text} \n {ru_ex.text}\n\n'
        except:
            continue
    return complete_string

def get_word():
    with open('eng_words.txt', 'r') as f:
        words = f.readlines()
        random_word = words[random.randint(0, 2990)]
    return random_word