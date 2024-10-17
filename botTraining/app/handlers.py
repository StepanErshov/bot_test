from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from app.middlewares import TestMiddleware
from app.dataBase import execute_db, print_db

router = Router()

router.message.outer_middleware(TestMiddleware())


class Reg(StatesGroup):
    name = State()
    number = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.reply(
        "Привет! Перед тем, как пользоваться ботом, нужно пройти регистрацию"
    )
    await reg_one(message, state)


@router.message(Reg.number, F.text.contains("Назад"))
async def cmd_start_for_reg(message: Message, state: FSMContext):
    if not message.text:
        return

    my_id = print_db(
        f"SELECT id FROM table_for_users WHERE telegram_id = '{message.from_user.id}'"
    )
    my_name = print_db(
        f"SELECT user_name FROM table_for_users WHERE telegram_id = '{message.from_user.id}'"
    )
    my_number = print_db(
        f"SELECT number_phone FROM table_for_users WHERE telegram_id = '{message.from_user.id}'"
    )

    await message.reply(
        f"Твой ID в Telegram: {message.from_user.id}\n"
        f"Твой ID в базе данных бота:{my_id}\n"
        f"Имя в Telegram: {message.from_user.first_name}\n"
        f"Твоё имя при регистрации: {my_name}\n"
        f"Фамилия: {message.from_user.last_name}\n"
        f"Номер телефона: {my_number}\n"
        f"Ваше пользовательское имя: {message.from_user.username}\n",
        reply_markup=kb.inline_keyboard,
    )


@router.message(lambda msg: msg.text == "Пошёл нахуй, бот" or msg.text == "Иди нахуй")
async def cmd_hui(message: Message):
    await message.answer("Сам иди нахуй!")


@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer("Это команда /help", reply_markup=kb.main)


@router.message(F.text == "Как дела?")
async def how_are_you(message: Message):
    await message.answer("Всё супер!")


@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(
        "Я пока что ещё не умею обрабатывать фото или видео(\nМогу сказать только ID\n"
        f"ID фото: {message.photo[-1].file_id}"
    )


@router.message(Command("take_photo"))
async def take_photo(message: Message):
    await message.answer_photo(
        photo="https://sun9-60.userapi.com/impg/RwL15WtVtSXjt_9Z1ZmJBEXCWd1oeeO9bmVjXg/ZaGUaKc9w28.jpg?size=500x439&quality=96&sign=0044146d956118c0b59c0019fd728979&type=album",
        caption="Пойман, петушара)",
    )


@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.answer("Вы выбрали каталог", show_alert=False)
    await callback.message.edit_text(
        "Это каталог автомобильных марок", reply_markup=await kb.inline_cars()
    )


@router.callback_query(F.data == "basket")
async def basket(callback: CallbackQuery):
    await callback.answer("Вы выбрали корзину", show_alert=False)
    await callback.message.edit_text(
        "Это ваша корзина покупок", reply_markup=await kb.inline_basket()
    )


@router.callback_query(F.data == "contacts")
async def show_contacts(callback: CallbackQuery):
    await callback.answer("Вы открыли контакты", show_alert=False)
    await callback.message.answer("Контакты", reply_markup=await kb.inline_contacts())


@router.callback_query(F.data == kb.BACK_BUTTON)
async def go_back(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите то, что ваш инетересует", reply_markup=kb.inline_keyboard
    )


@router.message(F.text == "Каталог")
async def phone(message: Message):
    await message.answer("Вы выбрали каталог", reply_markup=await kb.reply_cars())


@router.message(F.text == "Корзина")
async def phone(message: Message):
    await message.answer("Вы выбрали корзину", reply_markup=await kb.reply_food())


@router.message(F.text == "Телефон")
async def phone(message: Message):
    await message.answer("8-924-527-15-48")


@router.message(F.text == "Почта")
async def pochta(message: Message):
    await message.answer("SFS_stepan@mail.ru")


@router.message(F.text == "Назад")
async def back(message: Message, state: FSMContext):
    await cmd_start_for_reg(message, state)


@router.message(F.text == "Вернуться")
async def back_two(message: Message):
    await message.answer("Сделайте свой выбор", reply_markup=kb.main)


@router.message(Command("reg"))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer("Введите ваше имя")


@router.message(Reg.name)
async def reg_two(message: Message, state: FSMContext):
    name = message.text.strip()

    if not name:
        await message.answer("Пожалуйста, введите ваше имя.")
        return

    if message.text[0].islower():
        await message.answer("Имя должно начинаться с заглавной буквы")
        return

    if len(name) > 50:
        await message.answer("Имя не должно превышать 50 символов.")
        return

    if not name.isalpha():
        await message.answer("Пожалуйста, введите только буквы алфавита.")
        return

    await state.update_data(name=name)
    await state.set_state(Reg.number)
    await message.answer("Введите номер телефона")


@router.message(Reg.number)
async def two_thee(message: Message, state: FSMContext):
    number = message.text.strip()

    if not number.startswith("+7"):
        await message.answer("Номер телефона должен начинаться с +7")
        return

    if not number[3:].isdigit():
        await message.answer("Часть номера после +7 должна содержать только цифры")
        return

    if len(number) != 12:
        await message.answer("Номер телефона должен содержать 12 символов включая '+7'")
        return

    await state.update_data(number=number)
    data = await state.get_data()
    user_name = data["name"]
    num = data["number"]
    execute_db(
        f"INSERT INTO table_for_users(user_name, number_phone, telegram_id) VALUES('{user_name}', '{num}', '{message.from_user.id}')"
    )
    await message.answer(
        f"Регистрация завершена.\nИмя: {data['name']}\nНомер: {data['number']}\nВыберете то, что вас интересует",
        reply_markup=kb.inline_keyboard,
    )
    await state.clear()
