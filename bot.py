import telebot
import os

from dotenv import load_dotenv

from database import (
    check_chat_id_from_database,
    write_trello_to_database,
    check_size, update_database
)
from keyboards import (
    get_inline_boards_btn,
    get_inline_lists_btn,
    get_cards_btn
)
from utils import get_fullname

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode='html')


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Assalomu alaykum, ro'yxatdan o'tish uchun /register")


@bot.message_handler(commands=['update'])
def update_the_database(message):
    fullname = get_fullname(message)
    chat_id = message.chat.id

    bot.send_message(message.chat.id, "Qayta yuklanmoqda...")
    msg = update_database(chat_id, fullname)

    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['register'])
def register_handler(message):

    if not check_chat_id_from_database(message.chat.id):

        bot.send_message(message.chat.id, "Trello username kiriting: ")
        bot.register_next_step_handler(message, get_write_username_to_database)
    else:
        bot.send_message(message.chat.id, "Siz allaqchon ro'yxatdan o'tgansiz. Botdan foydalanishingiz mumkin /boards")


def get_write_username_to_database(message):

    fullname = get_fullname(message)
    username = message.text
    chat_id = message.chat.id

    bot.send_message(message.chat.id, "Yuklanmoqda....")

    write_trello_to_database(username, chat_id, fullname)

    if check_chat_id_from_database(message.chat.id):
        bot.send_message(message.chat.id, "Muvaffaqiyatli qo'shildi!")
    else:
        bot.send_message(message.chat.id, "Qo'shilmadi. Qaytadan urinib ko'ring /register")


@bot.message_handler(commands=["boards"])
def get_boards_bot(message):
    bot.send_message(message.chat.id, "Tanlang", reply_markup=get_inline_boards_btn("boards"))


@bot.callback_query_handler(lambda call: call.data.startswith("boards"))
def get_lists_bot(call):
    board_id = call.data.split("_")[1]

    if check_size(board_id) == 0:
        bot.send_message(call.message.chat.id, "Listlar yo'q!")
    else:
        bot.send_message(call.message.chat.id, "Tanlang", reply_markup=get_inline_lists_btn(board_id, "lists"))


@bot.callback_query_handler(lambda call: call.data.startswith("lists"))
def get_cards_bot(call):
    
    list_id = call.data.split("_")[1]
    bot.send_message(call.message.chat.id, get_cards_btn(list_id))


my_commands = [
    telebot.types.BotCommand("/start", "Botni ishga tushirish"),
    telebot.types.BotCommand("/register", "Ro'yxatdan o'tish"),
    telebot.types.BotCommand("/boards", "Doskalar"),
    telebot.types.BotCommand("/update", "Ma'lumotlarni qayta yuklash")
]

if __name__ == '__main__':
    print("started...")
    bot.set_my_commands(my_commands)
    bot.infinity_polling()
