import requests
from bs4 import BeautifulSoup


def get_weather(city):
    try:
        res = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=896831eabcb093fc849059be7ffbff60&lang=ru')
        data = res.json()
        return data
    except:
        return 'Извини, что-то пошло не так. Попробуй ещё раз.'

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