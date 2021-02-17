import telebot
from telebot import types as tp
import sys
from loguru import logger
import time
import lightshotparser
from configmanager import ConfigManager


config = ConfigManager()
bot = telebot.TeleBot(config.telegram_bot_token)

# MARKUPS
main_menu = tp.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=1)  # create selection keyboard
main_menu.add('📖 Random photo')
main_menu.add('⏱ Photo by hash')


@bot.message_handler(commands=['start', 'menu', 'help'])
def help_message(message):
    bot.send_message(message.from_user.id, '''👁‍🗨 *LightShot Parser Bot*.
Bot back-end was made by:

▫️ *@SepultureSE* _(Lightshot parser / Revisions)_
▫️ *@VPxyHNNmRi* _(Telegram Bot)_

*Usage*
Simply use buttons to get photos: `Random Photo` if you just want some fun, or `Photo by hash` if you're looking for the specific photo, that you have link to. Hash must be 6 characters long. Have fun
''', reply_markup=main_menu, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def bot_input(message):
    """ Реализация основного функционала бота """
    text = message.text
    user_id = message.from_user.id
    
    # возвращает случайный скриншот Lightshot
    if text == '📖 Random photo':
        photo_n_info = lightshotparser.LightshotParser.get_random_screenshot()
        
        bot.send_photo(user_id, photo_n_info.image, reply_markup=main_menu, 
                       caption=f'🔗 Link: {photo_n_info.link}')
        logger.info(f'{message.from_user.id}: Random screenshot has been sent')
        
    # возвращает скриншот Lightshot с указаным хешем
    if text == '⏱ Photo by hash':
        bot.send_message(message.from_user.id, '⌛️ *Send me hash*', parse_mode='Markdown')
        logger.info(f'{message.from_user.id}: Selected screenshot by hash')
        bot.register_next_step_handler(message, hash_search)
        
        
def hash_search(message):
    """ Реализация поиска скриншота по хешу """
    photo_n_info = lightshotparser.LightshotParser.get_screenshot_by_hash(message.text)
    
    if photo_n_info is None:
       bot.send_message(message.from_user.id, '❌ *Invalid hash. It must be 6 characters long*', reply_markup=main_menu, parse_mode='Markdown')
       logger.error(f'{message.from_user.id}: Invalid hash')
       return
   
    bot.send_photo(message.from_user.id, photo_n_info.image, caption=f'🔗 Link: {photo_n_info.link}')
    logger.info(f'{message.from_user.id}: Screenshot by hash has been sent')


if __name__ == '__main__':
    logger.add('resources/logging.log', format='{time} | {level} | {message}', level='DEBUG', rotation='5 MB', compression='zip')
    logger.info('Bot has been started')
    
    while True:
        try:
            bot.polling(none_stop=True)
        except KeyboardInterrupt:
            logger.critical('Exiting the program')
            sys.exit(0)
        except ConnectionError:
            logger.critical('No access to Telegram')
            time.sleep(15)
