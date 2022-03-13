import json

import vlc
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver
from aiogram.dispatcher.filters import Text
from selenium.webdriver.common.by import By
import time
import config
import requests
from bs4 import BeautifulSoup
import sqlite3
from db import DataBase

import playsound



import lxml


bot = Bot(token=config.TOKEN,parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot)
db = DataBase('db.db')

@dp.message_handler(commands='reg',commands_prefix='!/')
async def start(message: types.Message):
    if (not db.user_exists(message.message_id)):
        await bot.send_message(message.from_user.id, 'Укажите ваш ник')
        db.add_users(message.from_user.id)
        #await bot.send_message('Регистрация прошла успешно')
    else:
        await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы!')

@dp.message_handler(commands='subscribe',commands_prefix='!/')
async def start(message: types.Message):
    if (not db.update_subscribe(message.message_id)):
        db.add_subscribe(message.message_id)
        await bot.send_message(message.from_user.id, 'Подписка оформлена!')
    else:
        await bot.send_message(message.from_user.id, 'У вас есть активная подписка!')



@dp.message_handler(commands='start',commands_prefix='!/')
async def start(message: types.Message):
    await message.reply(f'Привет, {message.from_user.first_name}!')
    # player =vlc.MediaPlayer('Start.mp3')
    # player.play()

    buttons = ['📻 Радио','🎶 Музыка','Ютуб','Картинки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer('Выберите категорию', reply_markup=keyboard)

@dp.message_handler(Text(equals='Ютуб'))
async def play_youtube(message: types.Message):
    await message.answer('Введите название видеоролика')
    @dp.message_handler(content_types='text')
    async def search(message: types.Message):
        await message.answer('Подгружаю видеоролики...')
        driver = webdriver.Chrome('chromedriver/chromedriver.exe')
        driver.get('https://www.youtube.com/results?search_query=' + message.text)
        time.sleep(2)
        hrefs = driver.find_elements(By.ID,'video-title')
        for i in hrefs[:7]:
            name = i.text
            href = i.get_attribute('href')
            await message.answer(f'{name} - {href}')

# @dp.message_handler(commands='kurs',commands_prefix='!/')
# async def kurs(message: types.Message):
#     await message.answer("Загрузка...")


    # buttons = ['📻 Радио','🎶 Музыка','Ютуб','Картинки']
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard.add(*buttons)
    # await message.answer('Выберите категорию', reply_markup=keyboard)

@dp.message_handler(Text(equals='📻 Радио'))
async def play_radio(message: types.Message):
    await message.answer("Загрузка...")
    s = requests.Session()
    response = s.get('https://ru.hitmotop.com/radio')
    soup = BeautifulSoup(response.text, 'lxml')
    hrefs = soup.find('ul', class_='album-list muslist').find_all('div', class_='album-link')
    for i in hrefs[:10]:
        name = i.text.strip()
        href = i.get('data-url')
        await message.answer(f'{name} - {href}')


@dp.message_handler(commands='ban',commands_prefix='!/')
async def ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Эта команда должна быть ответом на сообщение!')
        return
    await message.bot.delete_message(chat_id=config.Chat_id, message_id= message.message_id)
    await message.bot.kick_chat_member(chat_id=config.Chat_id,user_id=message.message_id)
    await message.reply_to_message.reply("Сообщение удалено!")

def main():
    print('Бот готов к работе...')
    executor.start_polling(dp)


if __name__=='__main__':
    main()
