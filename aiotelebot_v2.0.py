# -*- coding: utf8 -*-
import asyncio
import logging
import aioschedule
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import api_fox_img
import business_logic


class OrderCity(StatesGroup):
    wait_city = State()
    wait_sign = State()



TOKEN = os.environ.get['TELETOKEN']
bot = Bot(token=TOKEN)  # Токен тестового бота testingspamobot

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
        await message.answer('Приветствую. Работает 04.09.22', reply_markup=help_kb)
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
        btn_fox = InlineKeyboardButton('Тест картинки лис', callback_data='/fox')
        btn_cat = InlineKeyboardButton('Тест картинки котиков', callback_data='/cat')

        btn_weather = InlineKeyboardButton('Узнать погоду', callback_data='/weather')
        write_kb = InlineKeyboardMarkup().add(btn_news).add(btn_horo).add(btn_weather) \
            .add(writeBtn).add(btn_fox).add(btn_cat)
        await message.answer('Пока что это все, что можно выбрать:', reply_markup=write_kb)
        await message.answer(
            f'Alpha_test. ver. 2.0, date 04.09.2022', reply_markup=help_kb)
    elif message.text == 'Donate':
        await message.answer('В тестовом режиме функция не работает. Жми HELP.')
        await message.answer(f'Alpha_test. ver. 2.0, date 04.09.2022', reply_markup=help_kb)
    else:
        await message.answer('Не пойму чего ты хочешь, нажми кнопку Help.')


@dp.callback_query_handler(lambda c: c.data == '/news_kk')
async def process_callback_news(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != 799592984:
        await bot.send_message(799592984, f'Кто-то нажал новости user_id - {callback_query.from_user.id}, '
                                          f'user name - {callback_query.from_user.username}')
    data_news = business_logic.news()
    await bot.send_message(callback_query.from_user.id, data_news, reply_markup=help_kb)


@dp.callback_query_handler(lambda c: c.data == '/weather')
async def callback_weather(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Погоду в каком городе хочешь узнать?')
    await OrderCity.wait_city.set()


async def weather_answer(message: types.Message, state: FSMContext):
    await state.update_data(city=message)
    city = await state.get_data()
    data_weather = business_logic.get_weather(city['city']['text'])
    try:
        await message.reply(f"В городе {city['city']['text']} температура {data_weather['main']['temp']} градусов, \n"
                            f"ощущается как {data_weather['main']['feels_like']}, \n"
                            f"{data_weather['weather'][0]['description']}, \n"
                            f"Ветер {data_weather['wind']['speed']} м/с.")
        await state.finish()
    except:
        await message.reply('Извини, что-то пошло не так, попробуй ещё раз, пожалуйста.')
        await state.finish()
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == '/horo')
async def callback_horo(callback_query: types.CallbackQuery):
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
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')

    horo_kb = InlineKeyboardMarkup(row_width=3).add(btn_aries, btn_taurus, btn_gemini). \
        add(btn_cancer, btn_leo, btn_virgo).add(btn_libra, btn_scorpio, btn_sagittarius) \
        .add(btn_capricorn, btn_aquarius, btn_pisces).add(btn_cancel)

    await bot.send_message(callback_query.from_user.id, 'Выбери знак зодиака: \n', reply_markup=horo_kb)
    await OrderCity.wait_sign.set()


async def horo_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(sign=callback_query.data)
    sign = await state.get_data()
    if sign['sign'] == 'cancel':
        await state.finish()
        await bot.send_message(callback_query.from_user.id, 'Хорошо, попробуй что-нибудь другое.')
    else:
        horo_sign = business_logic.horo(sign['sign'])
        try:
            await bot.send_message(callback_query.from_user.id, horo_sign)
            await state.finish()
        except:
            await bot.send_message(callback_query.from_user.id,
                                   'Извини, что-то пошло не так, попробуй снова, пожалуйста.')
            await state.finish()
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == '/fox')
async def test_fox(callback_query: types.CallbackQuery):
    img_name = api_fox_img.load_fox_img()
    img = open(f'{img_name}', 'rb')
    await bot.send_photo(callback_query.from_user.id, img, reply_markup=help_kb)
    api_fox_img.delete_fox_img(f'{img_name}')


async def send_fox():
    img_name = api_fox_img.load_fox_img()
    img = open(f'{img_name}', 'rb')
    await bot.send_photo(boss_id, img, reply_markup=help_kb)
    api_fox_img.delete_fox_img(f'{img_name}')

@dp.callback_query_handler(lambda c: c.data == '/cat')
async def test_cat(callback_query: types.CallbackQuery):
    img_name = api_fox_img.load_cat_img()
    img = open(f'{img_name}', 'rb')
    await bot.send_photo(callback_query.from_user.id, img, reply_markup=help_kb)
    api_fox_img.delete_cat_img(f'{img_name}')

async def send_cat():
    img_name = api_fox_img.load_cat_img()
    img = open(f'{img_name}', 'rb')
    await bot.send_photo(boss_id, img, reply_markup=help_kb)
    api_fox_img.delete_cat_img(f'{img_name}')


dp.register_message_handler(weather_answer, state=OrderCity.wait_city)
dp.register_callback_query_handler(horo_answer, state=OrderCity.wait_sign)
dp.register_callback_query_handler(callback_weather, state=OrderCity.wait_city)


# Отправка сообщений по времени
async def scheduler():
    aioschedule.every().day.at("09:10").do(send_fox)
    aioschedule.every().day.at("09:11").do(send_cat)
    aioschedule.every().day.at("09:12").do(send_fox)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(x):
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
