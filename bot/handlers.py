from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot import db

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привіт! Надішли фото їжі: я порахую КБЖВ.\n"
        "/help: допомога"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Сфотографуй тарілку зверху при доброму світлі й надішли сюди.")


@router.message(Command("undo"))
async def cmd_undo(message: Message):
    deleted = db.delete_last_meal(message.from_user.id)
    if deleted is None:
        await message.answer("Немає записів для видалення.")
        return
    await message.answer(f"Видалено: {deleted['dish']} ({deleted['calories']:.0f} ккал)")