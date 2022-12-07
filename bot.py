from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import *
import time
from config import get_config
import logging


conf = get_config()
admin = int(conf['admin_id'])
token = conf['bot_token']

bot = Bot(token, parse_mode='MARKDOWN') #Telegram bot token
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO, filename="log.log",filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


@dp.message_handler(commands=['adduser'])
async def add_user(message: types.Message):
    if message.chat.id == admin:
        try:
            id_user = message.text.split(' ')[1]
        except:
            await bot.send_message(message.chat.id, 'ты не ввел имя пользователя')
            return
        logging.info(f'Try add user {id_user}\n')
        if root_add(id_user) =='creat':
            with open(f'png/{id_user}.png', 'rb') as pfoto:
                await bot.send_photo(message.chat.id, pfoto)
            with open(f'conf/{id_user}.conf', 'rb') as file:
                await bot.send_document(message.chat.id, file)
            logging.info(f'User {id_user} added\n')
        else:
            await bot.send_message(message.chat.id, 'Не удалось добавить')
            logging.info(f'User {id_user} not added\n')


@dp.message_handler(commands=['remove'])
async def add_user(message: types.Message):
    if message.chat.id == admin:
        try:
            id_user = message.text.split(' ')[1]
        except:
            await message.answer('ты не ввел имя пользователя')
            return

        if check_in_db(id_user):
            deactive_user_db(id_user)
            await message.answer('Пользователь Удален')
        else:
            await message.answer('Пользователь нет в базе')


@dp.message_handler(commands=['client'])
async def see_client(message: types.Message):
    if message.chat.id == admin:
        clients = [f"[{client}](tg://user?id={client})" for client in client_list()]
        gifts = [f'<a href="tg://user?id={client}">{client}</a>' for client in gift_list()]
        client_text = 'Clients:\n' + '\n'.join(clients)
        gift_text = '\nGift client:\n' + '\n'.join(gifts)

        await message.answer(client_text)
        await message.answer(gift_text, parse_mode='HTML')


@dp.message_handler()
async def all_msg(msg: types.Message):
    button1 = InlineKeyboardButton("Подключить🚀", callback_data='connect')
    button2 = InlineKeyboardButton("Отключить", callback_data='remove')
    otvet1 = InlineKeyboardMarkup().add(button1, button2)


    if msg.chat.id == admin:
        if msg.forward_from != None:
            id_user = msg.forward_from.id
            await bot.send_message(msg.chat.id, f' Подключить {id_user}',reply_markup=otvet1)
        else:
            await bot.send_message(msg.chat.id, 'Перешли сообщение от того кого хочешь добавить.')

    else:
        logging.info(f'{msg.from_user.id} {msg.text} \n')
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
async def connect_user(callback_query: types.CallbackQuery):
    logging.info(f'{callback_query.from_user.id} connect \n')

    if callback_query.from_user.id != admin:
        if check_in_db(callback_query.from_user.id):
            with open(f'png/{callback_query.from_user.id}.png', 'rb') as pfoto:
                await bot.send_photo(callback_query.from_user.id, pfoto)
            with open(f'conf/{callback_query.from_user.id}.conf', 'rb') as file:
                await bot.send_document(callback_query.from_user.id, file)
        else:
            giftClient = str(callback_query.from_user.id)+'T'
            if check_gift(giftClient):
                if gift(giftClient):
                    with open(f'png/{giftClient}.png', 'rb') as pfoto:
                        await bot.send_photo(callback_query.from_user.id, pfoto)
                    with open(f'conf/{giftClient}.conf', 'rb') as file:
                        await bot.send_document(callback_query.from_user.id, file)
                    await bot.send_message(callback_query.from_user.id, "Тебе предоставлен тестовый период на один день, если захочешь продлить напиши @makcim646")
            else:
                await bot.send_message(callback_query.from_user.id, "Чтобы подключиться напиши @makcim646")


    else:
        id_user = callback_query.message.text.split()[-1]

        logging.info(f'{callback_query.from_user.id} try connect {id_user} \n')

        if check_in_db(id_user):
            await bot.send_message(callback_query.from_user.id, f'У пользователя {id_user} уже есть доступ', reply_markup=otvet3)
        else:
            if creat_new_user(id_user) == 'creat':
                await bot.send_message(callback_query.from_user.id, 'Пользователь добавлен')
                with open(f'png/{id_user}.png', 'rb') as pfoto:
                    await bot.send_photo(int(id_user), pfoto)
                with open(f'conf/{id_user}.conf', 'rb') as file:
                    await bot.send_document(int(id_user), file)
            else:
                await bot.send_message(callback_query.from_user.id, 'Что-то пошло не так, напиши @makcim646')




@dp.callback_query_handler(lambda c: c.data == 'remove')
async def remove_user(callback_query: types.CallbackQuery):
    logging.info(f'{callback_query.from_user.id} remove \n')
    id_user = callback_query.message.text.split()[-1]
    if check_in_db(id_user):
        deactive_user_db(id_user)
        await bot.send_message(callback_query.from_user.id, 'Пользователь Удален')
    else:
        await bot.send_message(callback_query.from_user.id, 'Пользователь нет в базе')


@dp.callback_query_handler(lambda c: c.data == 'remeber_conf')
async def remember_conf_user(callback_query: types.CallbackQuery):
    logging.info(f'{callback_query.from_user.id} remeber_conf \n')
    button1 = InlineKeyboardButton("Подключиться🚀", callback_data='connect')
    otvet2 = InlineKeyboardMarkup().add(button1)

    try:
        with open(f'png/{callback_query.from_user.id}.png', 'rb') as pfoto:
            await bot.send_photo(callback_query.from_user.id, pfoto)
        with open(f'conf/{callback_query.from_user.id}.conf', 'rb') as file:
            await bot.send_document(callback_query.from_user.id, file)
    except:
        await bot.send_message(callback_query.from_user.id, 'Ваше подключение остановлено', reply_markup=otvet2)


if __name__ == '__main__':
    executor.start_polling(dp)

