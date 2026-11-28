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


@router.message(Command("week"))
async def cmd_week(message: Message):
    days = db.get_week_stats(message.from_user.id)
    if not days:
        await message.answer("За останні 7 днів записів немає.")
        return
    lines = ["Статистика за 7 днів:"]
    for d in days:
        day = f"{d['date'][8:10]}.{d['date'][5:7]}"
        lines.append(
            f"{day}: {d['calories']:.0f} ккал "
            f"(Б {d['protein']:.0f} / Ж {d['fat']:.0f} / В {d['carbs']:.0f})"
        )
    total = sum(d["calories"] for d in days)
    lines.append(f"\nРазом: {total:.0f} ккал, у середньому {total / len(days):.0f} ккал/день")
    await message.answer("\n".join(lines))