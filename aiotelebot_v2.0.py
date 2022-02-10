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

bot = Bot(token='1097747087:AAG_GpsWo1Loj_0dfeF0EStQUEYwGH4xjI0') #Токен тестового бота testingspamobot

dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

btnHlp = KeyboardButton('Help')
btnDon = KeyboardButton('Donate')

help_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).row(btnHlp, btnDon)

greet_me = ['Хозяин', 'Повелитель', 'Иван Александрович', 'Мой создатель', 'Мой Руководитель']
boss_id = 799592984
greet_kris = ['Кристина Николаевна', 'Кристиночка', 'Лисичка', 'Королева', 'Красавица']
kris_id = 659386058

@dp.message_handler(commands='start')
async def start_using(message: types.Message):
    if message.from_user.id == 799592984:
        await message.answer('Приветствую. Работает 10.02.22', reply_markup=help_kb)
    else:
        await message.answer('Приветствую. Чтобы узнать что я умею нажми Help', reply_markup=help_kb)
        await bot.send_message(799592984, f'Кто-то нажал старт user_id - {message.from_user.id}, \n'
                                          f'user_name - {message.from_user.username}')









if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)