from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import types


class ButtonText:
    LIFE_PATH = "Рассчитать число жизненного пути"
    COMPOTOBILITY = "Проверить совместимость"
    NUMEROLOT_QUESTIONS = "Поговорить с нумерологом"
    BACK = "Назад"
    START = "/start"


def get_on_start_kb():
    button_life_path = KeyboardButton(text=ButtonText.LIFE_PATH)
    button_compatibility= KeyboardButton(text=ButtonText.COMPOTOBILITY)
    button_numerolog_questions = KeyboardButton(text=ButtonText.NUMEROLOT_QUESTIONS)
    buttons_row_one = [button_life_path, button_compatibility]
    buttons_row_second= [button_numerolog_questions]
    markup = (ReplyKeyboardMarkup
              (keyboard=[buttons_row_one, buttons_row_second],
               resize_keyboard=True)
              )
    return markup


def get_start_kb():
    start_button = KeyboardButton(text=ButtonText.START)
    buttons_row_start= [start_button]
    markup = (ReplyKeyboardMarkup(
        keyboard=[buttons_row_start],
        resize_keyboard=True
    ))


def get_start_inline_kb():
    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Начать", callback_data="start_action")
    keyboard.add(start_button)
    return keyboard

__all__ = ()
