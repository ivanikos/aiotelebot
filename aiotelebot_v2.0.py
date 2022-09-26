# -*- coding: utf8 -*-
import asyncio
import logging
import aioschedule
import datetime
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
    wait_english = State()
    wait_manual_word = State()


date_change = datetime.date.today().strftime("%d.%m.%Y")
# TOKEN = os.environ.get['TELETOKEN']

bot = Bot(token='1265062548:AAFqYKSGzXqCmAANEPfEN02SGj69rs9PLPA')

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
    if message.from_user.id == boss_id:
        await message.answer(f'Приветствую. Работает {date_change}', reply_markup=help_kb)
    else:
        await message.answer('Приветствую. Чтобы узнать что я умею нажми Help', reply_markup=help_kb)
        await bot.send_message(boss_id, f'Кто-то нажал старт user_id - {message.from_user.id}, \n'
                                        f'user_name - {message.from_user.username}')


@dp.message_handler()
async def help_command(message: types.Message):
    if message.text == 'Help':
        writeBtn = InlineKeyboardButton('Написать разработчику', url='telegram.me/ivanikos')
        btn_news = InlineKeyboardButton('Новости Краснодарского края', callback_data='/news_kk')
        btn_horo = InlineKeyboardButton('Узнать свой гороскоп', callback_data='/horo')
        btn_fox = InlineKeyboardButton('Фотку лисички', callback_data='/fox')
        btn_cat = InlineKeyboardButton('Фотку котика', callback_data='/cat')
        btn_quote = InlineKeyboardButton('Цитатку', callback_data='/quote')
        btn_eng_word = InlineKeyboardButton('Английские слова', callback_data='/eng_word')

        btn_weather = InlineKeyboardButton('Узнать погоду', callback_data='/weather')
        write_kb = InlineKeyboardMarkup().add(btn_news).add(btn_horo).add(btn_weather) \
            .add(btn_fox).add(btn_cat).add(btn_quote).add(btn_eng_word).add(writeBtn)
        await message.answer('Пока что это все, что можно выбрать:', reply_markup=write_kb)
        await message.answer(
            f'Alpha_test. ver. 2.0, date {date_change}', reply_markup=help_kb)
        if message.from_user.id == kris_id:
            await message.answer('Если напишешь мне в любой момент "Лисичку" или "Котика", пришлю тебе фото,'
                                 ' чтобы ты улыбнулась!')

    elif message.text == 'Лисичку' or message.text == 'лисичку':
        img_name = api_fox_img.load_fox_img()
        img = open(f'{img_name}', 'rb')
        await bot.send_photo(message.from_user.id, img, reply_markup=help_kb)
        api_fox_img.delete_fox_img(f'{img_name}')
    elif message.text == 'Котика' or message.text == 'котика':
        img_name = api_fox_img.load_cat_img()
        img = open(f'{img_name}', 'rb')
        await bot.send_photo(message.from_user.id, img, reply_markup=help_kb)
        api_fox_img.delete_cat_img(f'{img_name}')

    elif message.text == 'Donate':
        await message.answer('Просто кнопка, ничего не делает. Жми HELP.')
    else:
        await message.answer('Не пойму чего ты хочешь, нажми кнопку Help.')


@dp.callback_query_handler(lambda c: c.data == '/news_kk')
async def process_callback_news(callback_query: types.CallbackQuery):
    if callback_query.from_user.id != 799592984:
        await bot.send_message(799592984, f'Кто-то нажал новости user_id - {callback_query.from_user.id}, '
                                          f'user name - {callback_query.from_user.username}')
    data_news = business_logic.news()
    await bot.send_message(callback_query.from_user.id, data_news, reply_markup=help_kb)


@dp.callback_query_handler(lambda c: c.data == '/quote')
async def process_callback_news(callback_query: types.CallbackQuery):
    quote = business_logic.quote_all()
    await bot.send_message(callback_query.from_user.id, quote, reply_markup=help_kb)


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


# тест машины состояния на английские слова
@dp.callback_query_handler(lambda c: c.data == '/eng_word')
async def callback_eng_word(callback_query: types.CallbackQuery):
    btn_random_word = InlineKeyboardButton('Случайное слово', callback_data='random')
    btn_manual_word = InlineKeyboardButton('Напишу', callback_data='manual')

    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')

    horo_kb = InlineKeyboardMarkup(row_width=2).add(btn_random_word, btn_manual_word).add(btn_cancel)

    await bot.send_message(callback_query.from_user.id, 'Хочешь узнать случайное слово или '
                                                        'какое-то конкретное? \n', reply_markup=horo_kb)
    await OrderCity.wait_english.set()


@dp.callback_query_handler(state=OrderCity.wait_english)
async def eng_word_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(answer=callback_query.data)
    answer = await state.get_data()
    if answer['answer'] == 'cancel':
        await state.finish()
        await bot.send_message(callback_query.from_user.id, 'Хорошо, попробуй что-нибудь другое.')
    elif answer['answer'] == 'random':
        try:
            word = business_logic.get_word().strip()
            response = business_logic.english_words(word)
            await bot.send_message(callback_query.from_user.id, response)
            await state.finish()
        except:
            await bot.send_message(callback_query.from_user.id, 'Извини, что-то пошло не так, придётся попробовать '
                                                                'еще раз')
            await state.finish()

    elif answer['answer'] == 'manual':
        await bot.send_message(callback_query.from_user.id, 'Напиши слово на английском и я постараюсь его перевести:')
        await OrderCity.wait_manual_word.set()
    else:
        pass


@dp.message_handler(state=OrderCity.wait_manual_word)
async def eng_word_answer_manual(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    answer = await state.get_data()
    try:
        response = business_logic.english_words(answer['answer'])
        await bot.send_message(message.from_user.id, response)
        await state.finish()
    except:
        await bot.send_message(message.from_user.id, 'Извини, что-то пошло не так, придётся попробовать '
                                                            'еще раз')
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


async def send_fox_kris():
    img_name = api_fox_img.load_fox_img()
    img = open(f'{img_name}', 'rb')
    await bot.send_photo(kris_id, img, reply_markup=help_kb)
    api_fox_img.delete_fox_img(f'{img_name}')


async def send_cat_kris():
    img_name = api_fox_img.load_cat_img()
    img = open(f'{img_name}', 'rb')
    await bot.send_photo(kris_id, img, reply_markup=help_kb)
    api_fox_img.delete_cat_img(f'{img_name}')


async def morning_msg():
    greeting = 'Доброго утра, Иван Александрович!\n\n'
    data_weather = business_logic.get_weather('надым')
    weather_msg = f"На улице температура {data_weather['main']['temp']} градусов," \
                  f" \n ощущается как {data_weather['main']['feels_like']}," \
                  f" \n {data_weather['weather'][0]['description']}," \
                  f" \n Ветер {data_weather['wind']['speed']} м/с."

    horo_taurus = business_logic.horo('taurus')
    news_on_morning = business_logic.news()
    msg_final = greeting + 'Погода ' + weather_msg + '\n\nТвой гороскоп на сегодня:\n' + horo_taurus + \
                '\n\n' + '\nСвежие новости Краснодарского края:\n\n' + news_on_morning + '\n'
    await bot.send_message(boss_id, msg_final)


async def morning_msg_kris():
    greeting = 'Доброго утра, Кристиночка!\n\n'
    data_weather = business_logic.get_weather('Свободный')
    weather_msg = f"На улице температура {data_weather['main']['temp']} градусов," \
                  f" \n ощущается как {data_weather['main']['feels_like']}," \
                  f" \n {data_weather['weather'][0]['description']}," \
                  f" \n Ветер {data_weather['wind']['speed']} м/с."

    horo_taurus = business_logic.horo('taurus')
    news_on_morning = business_logic.news()
    msg_final = greeting + 'Погода ' + weather_msg + '\n\nТвой гороскоп на сегодня:\n' + horo_taurus + \
                '\n\n' + '\nСвежие новости Краснодарского края:\n\n' + news_on_morning + '\n'
    await bot.send_message(kris_id, msg_final)


async def quote_lao():
    quote = business_logic.quote_lao()
    await bot.send_message(boss_id, quote)


async def quote_lao_kris():
    quote = business_logic.quote_lao()
    await bot.send_message(kris_id, quote)


async def quote_all():
    quote = business_logic.quote_all()
    await bot.send_message(boss_id, quote)


async def quote_all_kris():
    quote = business_logic.quote_all()
    await bot.send_message(kris_id, quote)


async def quote_budda():
    quote = business_logic.quote_budda()
    await bot.send_message(boss_id, quote)


async def quote_budda_kris():
    quote = business_logic.quote_budda()
    await bot.send_message(kris_id, quote)


async def evening_msg():
    greeting = 'Доброй ночи, Иван Александрович!\n\n'
    quote = business_logic.quote_all()
    await bot.send_message(boss_id, greeting + quote)


async def evening_msg_kris():
    greeting = 'Доброй ночи, Кристиночка!\n\n'
    quote = business_logic.quote_all()
    await bot.send_message(kris_id, greeting + quote)

async def random_eng_word_learn():
    word = business_logic.get_word().strip()
    response = business_logic.english_words(word)
    await bot.send_message(boss_id, response)
async def random_eng_word_learn_kris():
    word = business_logic.get_word().strip()
    response = business_logic.english_words(word)
    await bot.send_message(kris_id, response)


dp.register_message_handler(weather_answer, state=OrderCity.wait_city)
dp.register_callback_query_handler(horo_answer, state=OrderCity.wait_sign)
dp.register_callback_query_handler(callback_weather, state=OrderCity.wait_city)

dp.register_callback_query_handler(eng_word_answer, state=OrderCity.wait_english)
dp.register_callback_query_handler(eng_word_answer_manual, state=OrderCity.wait_manual_word)


# Отправка сообщений по времени. Время МСК
async def scheduler():
    # Мои автосообщения
    aioschedule.every().day.at("06:10").do(morning_msg)
    aioschedule.every().day.at("06:12").do(quote_budda)
    aioschedule.every().day.at("10:30").do(quote_all)
    aioschedule.every().day.at("08:00").do(send_fox)
    aioschedule.every().day.at("08:10").do(random_eng_word_learn)
    aioschedule.every().day.at("10:00").do(send_cat)
    aioschedule.every().day.at("10:30").do(quote_all)
    aioschedule.every().day.at("11:00").do(random_eng_word_learn)
    aioschedule.every().day.at("15:00").do(send_fox)
    aioschedule.every().day.at("21:30").do(evening_msg)
    aioschedule.every().day.at("21:32").do(send_cat)
    aioschedule.every().day.at("21:33").do(random_eng_word_learn)

    # Автосообщения Кристине
    aioschedule.every().day.at("01:00").do(morning_msg_kris)
    aioschedule.every().day.at("01:02").do(quote_budda_kris)
    aioschedule.every().day.at("02:30").do(random_eng_word_learn_kris)
    aioschedule.every().day.at("03:00").do(send_fox_kris)
    aioschedule.every().day.at("06:30").do(send_cat_kris)
    aioschedule.every().day.at("09:00").do(quote_all_kris)
    aioschedule.every().day.at("10:30").do(random_eng_word_learn_kris)
    aioschedule.every().day.at("11:30").do(send_fox_kris)
    aioschedule.every().day.at("16:30").do(evening_msg_kris)
    aioschedule.every().day.at("16:32").do(quote_budda_kris)
    aioschedule.every().day.at("16:31").do(send_cat_kris)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(x):
    asyncio.create_task(scheduler())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
