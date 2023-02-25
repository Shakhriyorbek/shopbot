from data.loader import bot
from telebot.types import Message
from .text_handlers import start_register


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    text = 'Здравствуйте. Вас приветствует лучший бот интернет магазин'
    bot.send_message(chat_id, text)
    start_register(message)
