from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

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