from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging, os

with open('token.txt') as tok:
    t_token = tok.read().strip()

btnHlp = KeyboardButton('Help')
btnDon = KeyboardButton('Donate')

help_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).row(btnHlp, btnDon)

bot = Bot(token=t_token)  # Токен тестового бота testingspamobot

dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

boss_id = 799592984

@dp.message_handler(commands='start')
async def start_using(message: types.Message):
    if message.from_user.id == 799592984:
        await message.answer('Приветствую. Работает 12.02.22', reply_markup=help_kb)
    else:
        await message.answer('Приветствую. Чтобы узнать что я умею нажми Help', reply_markup=help_kb)
        await bot.send_message(799592984, f'Кто-то нажал старт user_id - {message.from_user.id}, \n'
                                          f'user_name - {message.from_user.username}')

@dp.message_handler()
async def help_command(message: types.Message):
    if message.from_user.id == 799592984:
        if message.text == 'Help':
            await message.answer('Работает пока что')
        elif message.text == 'Спать':
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            await message.answer('Я больше ничего не умею :(')



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)