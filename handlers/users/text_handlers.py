from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.reply import *
from keyboards.inline import *


def start_register(message: Message):
    chat_id = message.chat.id
    '''Вытащить пользователя по chat_id если что-то вышло - показать главное меню
    Если ничего не вышло - начать регистрацию'''
    user = db.get_user_by_id(chat_id)
    if user:
        '''Показать главное меню'''
        show_main_menu(message)
    else:
        msg = bot.send_message(chat_id, 'Отправьте свою имя и фамилию')
        bot.register_next_step_handler(msg, get_name_ask_phone)


def get_name_ask_phone(message: Message):
    chat_id = message.chat.id
    full_name = message.text
    msg = bot.send_message(chat_id, 'Отправьте свой номер телефона, нажав на кнопку',
                           reply_markup=generate_contact_button())
    bot.register_next_step_handler(msg, finish_register, full_name)


def finish_register(message: Message, full_name):
    chat_id = message.chat.id
    contact = message.contact.phone_number
    db.register_user(chat_id, full_name, contact)
    bot.send_message(chat_id, 'Регистрация прошла успешно')
    show_main_menu(message)


def show_main_menu(message: Message):
    chat_id = message.chat.id
    text = 'Что хотите сделать?'
    bot.send_message(chat_id, text, reply_markup=generate_main_menu())


@bot.message_handler(regexp='Сделать заказ 🛍')
def make_order(message: Message):
    chat_id = message.chat.id
    text = 'Выберите категорию товаров'
    bot.send_message(chat_id, text, reply_markup=generate_categories())


categories = db.get_categories()  # [('123',), ('123',)]
categories = [i[0] for i in categories]  # ['123', '123']


@bot.message_handler(func=lambda message: message.text in categories)
def reaction_to_category(message: Message):
    chat_id = message.chat.id
    text = 'Выберите товар: '
    your_choice = f'Вы выбрали категорию: {message.text}'
    bot.send_message(chat_id, your_choice, reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, text, reply_markup=generate_products_pagination(message.text))
