import asyncio
import mimetypes
import sys

from dotenv import load_dotenv

load_dotenv()
from bot.vision import analyze_food


async def main(paths):
    for path in paths:
        print(f"Аналізую {path}...", flush=True)
        mime_type = mimetypes.guess_type(path)[0] or "image/jpeg"
        with open(path, "rb") as f:
            result = await analyze_food(f.read(), mime_type)
        print(f"  → {result}", flush=True)


asyncio.run(main(sys.argv[1:] or ["test.jpg"]))