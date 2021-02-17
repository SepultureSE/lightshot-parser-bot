import telebot
from telebot import types as tp
import sys
import time
import lightshotparser

bot_input = 'TOKEN HERE'
bot = telebot.TeleBot(bot_input)


# MARKUPS
main_menu = tp.ReplyKeyboardMarkup(one_time_keyboard=True)  # create selection keyboard
main_menu.add('📖 Random photo')
main_menu.add('⏱ Photo by hash')


@bot.message_handler(commands=['start', 'menu', 'help'])
def help_message(message):
    bot.send_message(message.from_user.id, '''*LightShot Parser Bot*.
Bot back-end was made by
- @SepultureSE
- @VPxyHNNmRi
*Usage*
Simply use buttons to get photos: `Random Photo` if you just want some fun, or `Photo by hash` if you're looking for the specific photo, that you have link to. Have fun
''',reply_markup=main_menu, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def bot_input(message):
    text = message.text
    user_id = message.from_user.id
    
    if text == '📖 Random photo':
        photo_n_info = lightshotparser.LightshotParser.get_random_screenshot()
        if photo_n_info == None:
            bot.send_message(user_id, 'You aren\'t licky :(')
            return
        bot.send_photo(user_id, photo_n_info.image, reply_markup=main_menu)
        bot.send_message(user_id, photo_n_info.link, disable_web_page_preview=True)
    if text == '⏱ Photo by hash':
        bot.send_message(message.from_user.id, 'Send me hash')
        bot.register_next_step_handler(message, hash_search)
        photo_n_info = lightshotparser.LightshotParser.get_random_screenshot()
        
        
        
        
def hash_search(message):
    photo_n_info = lightshotparser.LightshotParser.get_screenshot_by_hash(message.text)
    if photo_n_info == None:
       bot.send_message(message.from_user.id, 'There is no image', reply_markup=main_menu)
       return
    bot.send_photo(message.from_user.id, photo_n_info.image)


if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(True)
        except KeyboardInterrupt:
            print("Exiting the program")
            sys.exit(0)
        except ConnectionError:
            print("No access to telegram")
            time.sleep(15)