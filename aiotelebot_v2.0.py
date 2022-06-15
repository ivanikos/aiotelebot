# -*- coding: utf8 -*-

import requests, os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging, requests, re, random
from bs4 import BeautifulSoup

class OrderCity(StatesGroup):
    wait_city = State()
    wait_sign = State()

#
# with open('token.txt') as tok:
#     t_token = tok.read().strip()

bot = Bot(token='1097747087:AAG_GpsWo1Loj_0dfeF0EStQUEYwGH4xjI0')  # Токен тестового бота testingspamobot

dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

btnHlp = KeyboardButton('Help')
btnDon = KeyboardButton('Donate')

help_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).row(btnHlp, btnDon)

greet_me = ['Хозяин', 'Повелитель', 'Иван Александрович', 'Мой создатель', 'Мой Руководитель']
boss_id = 799592984
greet_kris = ['Кристина Николаевна', 'Кристиночка', 'Лисичка', 'Королева', 'Красавица']
kris_id = 659386058

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


@dp.message_handler(commands='start')
async def start_using(message: types.Message):
    if message.from_user.id == 799592984:
        await message.answer('Приветствую. Работает 01.03.22', reply_markup=help_kb)
    else:
        await message.answer('Приветствую. Чтобы узнать что я умею нажми Help', reply_markup=help_kb)
        await bot.send_message(799592984, f'Кто-то нажал старт user_id - {message.from_user.id}, \n'
                                          f'user_name - {message.from_user.username}')


@dp.message_handler()
async def help_command(message: types.Message):
    if message.text == 'Help':
        writeBtn = InlineKeyboardButton('Написать разработчику', url='telegram.me/ivanikos')
        btn_news = InlineKeyboardButton('Новости Краснодарского края', callback_data='/news_kk')
        btn_horo = InlineKeyboardButton('Узнать свой гороскоп', callback_data='/horo')
        btn_exchange = InlineKeyboardButton('Узнать курс валют', callback_data='/exchange')
        btn_weather = InlineKeyboardButton('Узнать погоду', callback_data='/weather')
        write_kb = InlineKeyboardMarkup().add(btn_news).add(btn_horo).add(btn_weather).add(btn_exchange)\
            .add(writeBtn)
        await message.answer('Пока что это все, что можно выбрать:', reply_markup=write_kb)
        await message.answer(
            f'Alpha_test. ver. 2.0, date 15.02.2022', reply_markup=help_kb)
    elif message.text == 'Donate':
        await message.answer('В тестовом режиме функция не работает. Жми HELP.')
        await message.answer(f'Alpha_test. ver. 2.0, date 15.02.2022', reply_markup=help_kb)
    else:
        await message.answer('Не пойму чего ты хочешь, нажми кнопку Help.')

@dp.callback_query_handler(lambda c: c.data == '/news_kk')
async def process_callback_news(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != 799592984:
        await bot.send_message(799592984, f'Кто-то нажал новости user_id - {callback_query.from_user.id}, '
                                          f'user name - {callback_query.from_user.username}')
    data_news = news()
    await bot.send_message(callback_query.from_user.id, data_news, reply_markup=help_kb)

@dp.callback_query_handler(lambda c: c.data == '/weather')
async def callback_horo(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Погоду в каком городе хочешь узнать?')
    await OrderCity.wait_sign.set()

async def weather_answer(message: types.Message, state: FSMContext):
    await state.update_data(city=message)
    city = await state.get_data()
    data_weather = get_weather(city['city']['text'])
    try:
        await message.reply(f"В городе {city['city']['text']} температура {data_weather['main']['temp']} градусов, \n"
                            f"ощущается как {data_weather['main']['feels_like']}, \n"
                            f"{data_weather['weather'][0]['description']}, \n"
                            f"Ветер {data_weather['wind']['speed']} м/с.")
    except:
        await message.reply('Извини, что-то пошло не так, попробуй ещё раз, пожалуйста.')
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == '/horo')
async def callback_weather(callback_query: types.CallbackQuery):
    btn_aries = InlineKeyboardButton('Овен', callback_data='aries')
    btn_taurus = InlineKeyboardButton('Телец', callback_data='taurus')
    btn_gemini = InlineKeyboardButton('Близнецы', callback_data='gemini')
    btn_cancer = InlineKeyboardButton('Рак', callback_data='cancer')
    btn_leo = InlineKeyboardButton('Лев', callback_data='leo')
    btn_virgo = InlineKeyboardButton('Дева', callback_data='virgo')
    btn_libra = InlineKeyboardButton('Весы', callback_data='libra')
    btn_scorpio = InlineKeyboardButton('Скорпион', callback_data='scorpio')
    btn_sagittarius = InlineKeyboardButton('Стрелец', callback_data='sagittarius')
    btn_capricorn = InlineKeyboardButton('Козерог', callback_data='capricorn')
    btn_aquarius = InlineKeyboardButton('Водолей', callback_data='aquarius')
    btn_pisces = InlineKeyboardButton('Рыбы', callback_data='pisces')

    horo_kb = InlineKeyboardMarkup(row_width=3).add(btn_aries, btn_taurus, btn_gemini).\
        add(btn_cancer, btn_leo, btn_virgo).add(btn_libra, btn_scorpio, btn_sagittarius)\
        .add(btn_capricorn, btn_aquarius, btn_pisces)

    await bot.send_message(callback_query.from_user.id, 'Выбери знак зодиака: \n', reply_markup=horo_kb)
    await OrderCity.wait_sign.set()

async def horo_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(sign=callback_query.data)
    sign = await state.get_data()
    horo_sign = horo(sign['sign'])
    try:
        await bot.send_message(callback_query.from_user.id, horo_sign)
        await state.finish()
    except:
        await bot.send_message(callback_query.from_user.id, 'Извини, что-то пошло не так, попробуй снова, пожалуйста.')

@dp.callback_query_handler(lambda c: c.data == '/horo')
async def callback_horo(callback_query: types.CallbackQuery):
    # '/aries - Овен \n'
    # '/taurus - Телец \n'
    # '/gemini - Близнецы\n'
    # '/cancer - Рак\n'
    # '/leo - Лев\n'
    # '/virgo - Дева\n'
    # '/libra - Весы\n'
    # '/scorpio - Скорпион\n'
    # '/sagittarius - Стрелец\n'
    # '/capricorn - Козерог\n'
    # '/aquarius - Водолей\n'
    # '/pisces - Рыбы')

    btn_aries = InlineKeyboardButton('Aries', 'aries')
    horo_kb = InlineKeyboardMarkup().add(btn_aries)
    await bot.send_message(callback_query.from_user.id, 'Выбери знак зодиака: \n', reply_markup=horo_kb)
    await OrderCity.wait_sign.set()

async def callback_horo_ans(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(a=callback_query)
    a = await state.get_data()
    print(a)
    print(callback_query)
    print('зашел')

dp.register_message_handler(callback_horo_ans, state=OrderCity.wait_sign)

dp.register_message_handler(weather_answer, state=OrderCity.wait_city)
dp.register_callback_query_handler(horo_answer, state=OrderCity.wait_sign)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
