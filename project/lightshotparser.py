from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from io import BytesIO
import requests
import sys
import numpy as np
from abc import ABC, abstractmethod


PARSER_ALPHABET_CONST = '0abcdefghijklmnopqrstuvwxyz123456789'


class ScreenshotObject(object):
    """ Объект скриншота """
    def __init__(self, image: object, link: str):
        self.image = image  # атрибут изображения скриншота
        self.pillow_image = BytesIO(image)  # атрибут изображения скриншота для библиотеки Pillow
        self.link = link  # ссылка на скриншот в Lightshot
        self.search_date = datetime.now()  # дата поиска данного скриншота
        
    def __str__(self):
        # вывод данных о скриншоте через print()
        return f'\nScreenshot Data\n{"-" * 10}\nLink: {self.link}\nSearch Date: {self.search_date}'


class LightshotParser(ABC):
    """ Абстрактный класс парсера данных с Lightshot """ 
    @abstractmethod
    def get_random_screenshot() -> object:
        """ Возвращает случайный скриншот """
        screenshot_id_hash = str()
        
        # генерирует хеш скриншота так, чтобы 0 не являлся первым символом
        for i in (range(6)):
            if i == 0:
                screenshot_id_hash += PARSER_ALPHABET_CONST[1:][np.random.randint(len(PARSER_ALPHABET_CONST) - 1)]
            else:
                screenshot_id_hash += PARSER_ALPHABET_CONST[np.random.randint(len(PARSER_ALPHABET_CONST))]
        
        generated_link = f'https://prnt.sc/{screenshot_id_hash}'  # итоговый вариант lightshot ссылки с хешем
        response = requests.get(generated_link, headers={'User-Agent': UserAgent().random})  # запрос на сайт со скриншотом
        soup = BeautifulSoup(response.text, features='lxml')  # экземпляр bs4 парсера
        
        # ссылка на изображение скриншота 
        try:
            lightshot_img_path = soup.find('div', attrs={'class': 'image-container image__pic js-image-pic'}).find('img')['src']
        except AttributeError:
            LightshotParser.get_random_screenshot()
        
        # если такого скриншота на сервере не существует, возвращает None
        try:
            image = requests.get(lightshot_img_path).content  # само изображение скриншота
            return ScreenshotObject(image, generated_link)
        except requests.exceptions.MissingSchema:
            return None
    
    @abstractmethod
    def get_screenshot_by_hash(image_hash: str) -> object:
        """ Возвращает определенный скриншот по его хэшу """
        assert image_hash[0] != '0', 'Первым символом хеша не может быть 0'
     
        # запрос на сайт со скриншотом с определенным хешем
        response = requests.get(f'https://prnt.sc/{image_hash}', headers={'User-Agent': UserAgent().random})
        soup = BeautifulSoup(response.text, features='lxml')  # экземпляр bs4 парсера
        
        # ссылка на изображение скриншота
        try:
            lightshot_img_path = soup.find('div', attrs={'class': 'image-container image__pic js-image-pic'}).find('img')['src']
        except AttributeError:
            LightshotParser.get_screenshot_by_hash(image_hash)
        
        # если такого скриншота на сервере не существует, возвращает None
        try:
            image = requests.get(lightshot_img_path).content  # само изображение скриншота
            return ScreenshotObject(image, f'https://prnt.sc/{image_hash}')
        except requests.exceptions.MissingSchema:
            return None