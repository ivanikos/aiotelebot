# -*- coding: utf8 -*-

import requests, telebot, re, os
import time, pytube
from multiprocessing.context import Process
import schedule
import random
from bs4 import BeautifulSoup
from telebot import types
import cfscrape
from lxml import html

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging, requests, re, random
from bs4 import BeautifulSoup

class OrderCity(StatesGroup):
    wait_city = State()


with open('token.txt') as tok:
    t_token = tok.read().strip()

bot = Bot(token=t_token)  # Токен тестового бота testingspamobot

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
        await message.answer('Приветствую. Работает 10.02.22', reply_markup=help_kb)
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
async def callback_weather(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Погоду в каком городе ты хотел бы узнать?')
    await OrderCity.wait_city.set()


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


dp.register_message_handler(weather_answer, state=OrderCity.wait_city)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
