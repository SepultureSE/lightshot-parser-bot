from configparser import ConfigParser
import os


DEFAULT_CONFIG_NAME_CONST = 'config.ini'


class ConfigManager(object):
    """ Класс менеджера конфиг. файлов """
    def __new__(cls, *args, **kwargs):
        """ Реализация паттерна Singleton """
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigManager, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.__parser = ConfigParser()
        
        # создает конфиг. файл, если он отсутствует
        if not os.path.exists(DEFAULT_CONFIG_NAME_CONST):
            self.__create_config_file()
            
        self.__parser.read(DEFAULT_CONFIG_NAME_CONST)
        
        self.telegram_bot_token = self.__parser.get('BOT SETTINGS', 'token')
        
        self.parser_is_logging = self.__parser.getboolean('PARSER SETTINGS', 'logging')
        
        self.project_github_repository = self.__parser.get('PROJECT INFORMATION', 'github_repository')
        self.project_version = self.__parser.get('PROJECT INFORMATION', 'version')
        self.project_license = self.__parser.get('PROJECT INFORMATION', 'license')
            
    def __create_config_file(self):
        """ Создает конфигурационный файл """
        # конфигурация по-умолчанию Telegram бота
        self.__parser.add_section('BOT SETTINGS')
        self.__parser.set('BOT SETTINGS', 'token', '')
        
        # конфигурация парсера
        self.__parser.add_section('PARSER SETTINGS')
        self.__parser.set('PARSER SETTINGS', 'logging', 'false')
        
        # информация о проекте
        self.__parser.add_section('PROJECT INFORMATION')
        self.__parser.set('PROJECT INFORMATION', 'github_repository', 'https://github.com/SepultureSE/lightshot-parser-bot')
        self.__parser.set('PROJECT INFORMATION', 'version', '')
        self.__parser.set('PROJECT INFORMATION', 'license', 'GNU General Public License v3.0')
        
        with open(DEFAULT_CONFIG_NAME_CONST, 'w') as config_file:
            self.__parser.write(config_file)