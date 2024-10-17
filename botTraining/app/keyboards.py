from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

BACK_BUTTON = "Назад"

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каталог")],
        [KeyboardButton(text="Корзина"), KeyboardButton(text="Контакты")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберете пункт меню.",
)

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
        [
            InlineKeyboardButton(text="Корзина", callback_data="basket"),
            InlineKeyboardButton(text="Контакты", callback_data="contacts"),
        ],
    ]
)

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Youtube", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            )
        ]
    ]
)

cars = ["Tesla", "Mercedes", "BMW", "Toyota"]
urls_for_car = [
    "https://ru.wikipedia.org/wiki/Tesla",
    "https://ru.wikipedia.org/wiki/Mercedes-Benz",
    "https://ru.wikipedia.org/wiki/BMW",
    "https://ru.wikipedia.org/wiki/Toyota",
]

food = ["Banana", "Orange", "Milk", "Water", "Oil", "Pasta"]
urls_for_food = [
    "https://ru.wiktionary.org/wiki/banana",
    "https://ru.wikipedia.org/wiki/Orange",
    "https://en.wikipedia.org/wiki/Milk",
    "https://en.wikipedia.org/wiki/Water",
    "https://en.wikipedia.org/wiki/Oil",
    "https://ru.wikipedia.org/wiki/Pasta",
]

contacts = ["Телефон", "Почта"]
val_contacts = ["+7-924-527-15-48", "SFS_stepan@mail.ru"]


async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car, url in zip(cars, urls_for_car):
        keyboard.add(InlineKeyboardButton(text=car, url=url))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=BACK_BUTTON))
    return keyboard.adjust(2).as_markup()


async def inline_basket():
    keyboard_1 = InlineKeyboardBuilder()
    for foods, urls in zip(food, urls_for_food):
        keyboard_1.add(InlineKeyboardButton(text=foods, url=urls))
    keyboard_1.add(InlineKeyboardButton(text="Назад", callback_data=BACK_BUTTON))
    return keyboard_1.adjust(2).as_markup()


async def inline_contacts():
    keyboard_3 = InlineKeyboardBuilder()
    for contacts, val_contacts in zip(food, urls_for_food):
        keyboard_3.add(InlineKeyboardButton(text=contacts, callback_data=val_contacts))
    keyboard_3.add(InlineKeyboardButton(text="Назад", callback_data=BACK_BUTTON))
    return keyboard_3.adjust(2).as_markup()


async def reply_cars():
    keybord1 = ReplyKeyboardBuilder()
    for car, url in zip(cars, urls_for_car):
        keybord1.add(KeyboardButton(text=car, url=url))
    keybord1.add(KeyboardButton(text="Вернуться", callback_data=BACK_BUTTON))
    return keybord1.as_markup(resize_keyboard=True)


async def reply_food():
    keybord1 = ReplyKeyboardBuilder()
    for foods, urls in zip(food, urls_for_car):
        keybord1.add(KeyboardButton(text=foods, url=urls))
    keybord1.add(KeyboardButton(text="Вернуться", callback_data=BACK_BUTTON))
    return keybord1.as_markup(resize_keyboard=True)


async def reply_contacts():
    keyboard_2 = ReplyKeyboardBuilder()
    keyboard_2.add(KeyboardButton(text="Телефон"))
    keyboard_2.add(KeyboardButton(text="Почта"))
    keyboard_2.add(KeyboardButton(text="Вернуться", callback_data=BACK_BUTTON))
    return keyboard_2.as_markup(resize_keyboard=True)


async def inline_contacts():
    keyboard_2 = ReplyKeyboardBuilder()
    keyboard_2.add(KeyboardButton(text="Телефон"))
    keyboard_2.add(KeyboardButton(text="Почта"))
    keyboard_2.add(KeyboardButton(text="Назад", callback_data=BACK_BUTTON))
    return keyboard_2.as_markup(resize_keyboard=True)
