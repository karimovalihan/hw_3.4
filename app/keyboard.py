from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton

from app.db import *

inline_end_button = [
    [InlineKeyboardButton(text='Подтвердить'), InlineKeyboardButton(text='Отменить', callback_data='about')]
]

inline_start_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_end_button)

inline_about = InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(), InlineKeyboardButton()]
])

async def inline_direction():
    directions = ()
    keyboard = InlineKeyboardBuilder()
    for direction in directions:
        keyboard.add(InlineKeyboardButton(text=direction, callback_data=f'dir_{direction}'))
    return keyboard.adjust(2).as_markup()

