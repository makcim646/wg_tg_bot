from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import *
import time
from config import telegram_token, admin


bot = Bot(telegram_token) #Telegram bot token
dp = Dispatcher(bot)


@dp.message_handler(commands=['adduser'])
async def add_user(message: types.Message):
    if message.chat.id in admin:
        try:
            id_user = message.text.split(' ')[1]
        except:
            await bot.send_message(message.chat.id, 'ты не ввел имя пользователя')
            return
        log(f'{time.ctime()} Try add user {id_user}\n')
        if root_add(id_user) =='creat':
            with open(f'png/{id_user}.png', 'rb') as pfoto:
                await bot.send_photo(message.chat.id, pfoto)
            with open(f'conf/wg0-client-{id_user}.conf', 'rb') as file:
                await bot.send_document(message.chat.id, file)
            log(f'{time.ctime()} User {id_user} added\n')
        else:
            await bot.send_message(message.chat.id, 'Не удалось добавить')

@dp.message_handler()
async def change_user(msg: types.Message):
    button1 = InlineKeyboardButton("Подключить🚀", callback_data='connect')
    otvet1 = InlineKeyboardMarkup().add(button1)


    if msg.chat.id in admin:
        if msg.forward_from != None:
            id_user = msg.forward_from.id
            await bot.send_message(msg.chat.id, f' Подключить {id_user}?',reply_markup=otvet1)
        else:
            await bot.send_message(msg.chat.id, 'Перешли сообщение от того кого хочешь добавить.')

    else:
        log(f'{time.ctime()} {msg.from_user.id} {msg.text} \n'.encode('utf-8'))
        msg_text = '''1.Для подключения скачай приложение wireguard
    [Wireguard Android](https://play.google.com/store/apps/details?id=com.wireguard.android&hl=ru&gl=US)
    [Wireguard Ios](https://apps.apple.com/us/app/wireguard/id1441195209)
    [wireguard Windos](https://www.wireguard.com/install/)
    2.В боте нажмите кнопку Подключиться🚀 .
    3.Бот вам отправит QR-code и конфигурационый файл.
    4.В приложение отсканируйте QR-code или скачайте конфигурационый файл и
    импортируйте его через приложение.
    '''

        button1 = InlineKeyboardButton("Подключиться🚀", callback_data='connect')
        button2 = InlineKeyboardButton("Напомнить настройки💾", callback_data='remeber_conf')

        otvet1 = InlineKeyboardMarkup(row_width=2).add(button1, button2)

        await bot.send_message(msg.from_user.id, msg_text, disable_web_page_preview=True, reply_markup=otvet1, parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'connect')
async def process_callback_button1(callback_query: types.CallbackQuery):
    log(f'{time.ctime()} {callback_query.from_user.id} connect \n')

    button1 = InlineKeyboardButton("Продлить🚀", callback_data='to_extend')
    otvet3 = InlineKeyboardMarkup().add(button1)

    if callback_query.from_user.id not in admin:
        if check_in_db(callback_query.from_user.id):
            with open(f'png/{callback_query.from_user.id}.png', 'rb') as pfoto:
                await bot.send_photo(callback_query.from_user.id, pfoto)
            with open(f'conf/wg0-client-{callback_query.from_user.id}.conf', 'rb') as file:
                await bot.send_document(callback_query.from_user.id, file)
        else:
            await bot.send_message(callback_query.from_user.id, "Чтобы подключиться напиши @makcim646")


    else:
        id_user = callback_query.message.text.split()[-1]
        
        log(f'{time.ctime()} {callback_query.from_user.id} try connect {id_user} \n')

        if check_in_db(id_user):
            await bot.send_message(callback_query.from_user.id, f'У пользователя {id_user} уже есть доступ', reply_markup=otvet3)
        else:
            if creat_new_user(id_user) == 'creat':
                await bot.send_message(callback_query.from_user.id, 'Пользователь добавлен')
            else:
                await bot.send_message(callback_query.from_user.id, 'Что-то пошло не так, напиши @makcim646')




@dp.callback_query_handler(lambda c: c.data == 'remeber_conf')
async def process_callback_button1(callback_query: types.CallbackQuery):
    log(f'{time.ctime()} {callback_query.from_user.id} remeber_conf \n')
    print(callback_query.from_user.id, 'remeber_conf')
    button1 = InlineKeyboardButton("Подключиться🚀", callback_data='connect')
    otvet2 = InlineKeyboardMarkup().add(button1)

    try:
        with open(f'png/{callback_query.from_user.id}.png', 'rb') as pfoto:
            await bot.send_photo(callback_query.from_user.id, pfoto)
        with open(f'conf/wg0-client-{callback_query.from_user.id}.conf', 'rb') as file:
            await bot.send_document(callback_query.from_user.id, file)
    except:
        await bot.send_message(callback_query.from_user.id, 'Ваше подключение остановлено', reply_markup=otvet2)


if __name__ == '__main__':
    executor.start_polling(dp)
