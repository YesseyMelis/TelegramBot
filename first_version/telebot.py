import telegram
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
import logging
from scrap import open_page, parse_crypto, parse_top_crypto
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
url = 'https://myfin.by/crypto-rates/'

def get_tops():
    page = open_page(url)
    tops = parse_top_crypto(page)
    return tops
tops = get_tops()

def get_crypto(name):
    mainText = "        Weighted average rate:           \n%s        %s\n  Changes for:    \nday:  %s      \nweek:  %s      \nmonth:  %s     \n6-month:  %s"
    c_url = url + name.lower()
    c_page = open_page(c_url)
    c_data = parse_crypto(c_page)
    c_text = mainText%(c_data[0]['price'], c_data[0]['up'], c_data[0]['day'], c_data[0]['week'], c_data[0]['month'], c_data[0]['sixmonth'])
    
    return c_text


bot = telegram.Bot(token='TOKEN')
updater = Updater(token="TOKEN")
dispatcher = updater.dispatcher


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def start(bot, update):
    but = []
    for i in range(len(tops[0])):
        but.append(KeyboardButton(tops[0][i]))
    reply = ReplyKeyboardMarkup(build_menu(but, n_cols=3))
    bot.sendMessage(chat_id=update.message.chat_id, text = "what you want to know?", reply_markup=reply)

def echo(bot, update):
    text = update.message.text
    idx = tops[0].index(text)
    chouse = tops[1][idx]
    bot.send_message(chat_id=update.message.chat_id, text = get_crypto(chouse))

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater.start_polling()