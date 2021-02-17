import telebot
from lightshotparser import LightshotParser


bot = telebot.TeleBot(token='1636954625:AAF2-s8UFPTLE3i3KZQAS41IdvzvApTNkko')

@bot.message_handler(commands=['start'])
def on_start(message):
    screenshot = LightshotParser.get_random_screenshot()
    bot.send_photo(message.from_user.id, screenshot.image)
    
    
bot.polling()