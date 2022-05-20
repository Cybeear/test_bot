from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import Datapacks



def fao_keyboard():
	keyboard = InlineKeyboardMarkup()
	for i in range(0, len(Datapacks.fao)):
		button = InlineKeyboardButton(Datapacks.fao[i+1], callback_data=f"fao_btn{i}")       
		keyboard.add(button)
	return keyboard


def work_keyboard():
	keyboard = InlineKeyboardMarkup()
	for i in range(0, len(Datapacks.vacancies)):
		button = InlineKeyboardButton(Datapacks.vacancies_name[i+1], callback_data=f"work_btn{i}")
		keyboard.add(button)
	return keyboard


def menu_keyboard():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton('Меню'))
	keyboard.row(KeyboardButton('Гід'),KeyboardButton('Допомога'), KeyboardButton('ФАО'))
	keyboard.row(KeyboardButton('Відіслати резюме'),KeyboardButton('Реєстрація'), KeyboardButton('Робота'), )
	keyboard.row(KeyboardButton('Видалити анкету'), KeyboardButton('Переглянути анкету'))

	return keyboard

def file_menu_keyboard():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton('Меню'))
	return keyboard


def reg_keyboard():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton('Меню'))
	keyboard.row(KeyboardButton('ПІБ'), KeyboardButton('Вік'))
	keyboard.row(KeyboardButton('Навички'), KeyboardButton('Номер телефону'))
	keyboard.add(KeyboardButton('Завершити реєстрацію'), KeyboardButton('Відміна'))
	return keyboard
