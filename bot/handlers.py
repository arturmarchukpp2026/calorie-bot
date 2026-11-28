import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot import db
from bot.vision import analyze_food

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


@router.message(Command("today"))
async def cmd_today(message: Message):
    t = db.get_today_totals(message.from_user.id)
    if t["count"] == 0:
        await message.answer("Сьогодні ще нічого не записано.")
        return
    await message.answer(
        f"Сьогодні ({t['count']} прийомів їжі):\n"
        f"{t['calories']:.0f} ккал · Б {t['protein']:.0f} г · "
        f"Ж {t['fat']:.0f} г · В {t['carbs']:.0f} г"
    )


@router.message(F.photo)
async def on_photo(message: Message):
    status = await message.answer("Аналізую фото…")
    file = await message.bot.download(message.photo[-1])  # найбільший розмір
    try:
        meal = await analyze_food(file.read())
    except Exception:
        logging.exception("Помилка розпізнавання фото")
        await status.edit_text("Не вдалося розпізнати. Спробуй ще раз через хвилину.")
        return

    if not meal.get("is_food"):
        await status.edit_text("Не бачу на фото їжі. Спробуй інше фото.")
        return

    db.add_meal(message.from_user.id, meal)
    today = db.get_today_totals(message.from_user.id)
    await status.edit_text(
        f"{meal['dish']} (~{meal['weight_g']} г)\n"
        f"Калорії: {meal['calories']} ккал\n"
        f"Білки: {meal['protein']} г · Жири: {meal['fat']} г · Вуглеводи: {meal['carbs']} г\n\n"
        f"Збережено. Сьогодні разом: {today['calories']:.0f} ккал\n"
        "Помилився? /undo"
    )