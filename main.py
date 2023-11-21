import telebot
from config import TOKEN
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.first_name or message.from_user.username
    text = f'Здравствуйте, {user}!'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message):
    text = '''Для конвертации валюты необходимо ввести команду в следующем формате:
<имя исходной валюты> <имя целевой валюты> <количество исходной валюты>
Доступные валюты: доллар, евро, рубль'''
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        command = message.text.lower().split(' ')
        if len(command) != 3:
            raise APIException('Неверный формат команды')
        source, dest, volume = command
        result = Converter.get_price(source, dest, volume)
    except APIException as ex:
        bot.reply_to(message, f'400, Bad Request: {ex}')
    except Exception as ex:
        bot.reply_to(message, f'500, Internal Server Error: {ex}')
    else:
        bot.reply_to(message, f'{volume} {source} = {result} {dest}')

bot.polling()
