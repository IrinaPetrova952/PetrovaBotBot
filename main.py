import telebot
import requests
import json

TOKEN = '5690097715:AAF39NOBA3mRBqAiCngqfrfFo_f55h4o67w'

bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB',
}

class ConvertionException(Exception):
    pass

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите наименование валюты, в какую валюту перевести и количество. ' \
           'Список доступных валют: команда /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) > 3:
        raise ConvertionException('Слишком много параметров/')

    quote, base, amount = message.text.split(' ')

    if quote == base:
        raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    text = json.loads(r.content)[keys[base]]
    # total_base = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()