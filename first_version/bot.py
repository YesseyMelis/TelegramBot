import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
from scrap import open_page, parse_crypto

url = 'https://myfin.by/crypto-rates/bitcoin'
page = open_page(url)
json = parse_crypto(page)


bot = telegram.Bot(token='***')
updater = Updater(token='***')
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi, man!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=json)

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
updater.start_polling()
updater.idle()
