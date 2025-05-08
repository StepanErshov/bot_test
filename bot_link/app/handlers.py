from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
from app.bot import bot 

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Прежде чем получить информацию, нужно быть подписанным на источники ниже", reply_markup=kb.inline_keyboard)

@router.callback_query(F.data == "check_subscription")
async def check_sub(callback: CallbackQuery):
    user_id = callback.from_user.id
    subscribed_channels = []
    channels = ["@shutimshutky", "@skvortsov_IT"]

    for channel in channels:
        try:
            chat_member = await bot.get_chat_member(channel, user_id)
            if chat_member.status in ['member', 'administrator', 'creator']:
                subscribed_channels.append(channel)
        except Exception as e:
            print(f"Ошибка при проверке канала {channel}: {e}")

    if chat_member.status in ['member', 'administrator', 'creator']:
        await callback.answer("Вы подписаны на канал!")
        await get_file(callback.message)
    else:
        await callback.answer("Вы не подписаны на каналы.")

@router.message(Command("get_file"))
async def get_file(message: Message):
    file = open("C:/Users/79245/Desktop/Shedule-innoglobalhack24.pdf", "+r")
    await message.answer_document(document=file)