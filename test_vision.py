import asyncio
from dotenv import load_dotenv

load_dotenv()
from bot.vision import analyze_food

with open("test.jpg", "rb") as f:
    print(asyncio.run(analyze_food(f.read())))