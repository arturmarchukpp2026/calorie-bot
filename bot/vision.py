import asyncio
import json
import os

from google import genai
from google.genai import errors, types

# Моделі по черзі: якщо одна перевантажена, не відповідає або ліміт — пробуємо наступну
MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]
TIMEOUT_SECONDS = 40  # скільки чекати відповіді від однієї моделі

PROMPT = """Ти дієтолог. Визнач страву на фото, оціни вагу всієї порції в грамах
і її КБЖВ (на всю порцію, не на 100 г).
Відповідай ЛИШЕ JSON такого вигляду, числа — цілі:
{"is_food": true, "dish": "назва українською", "weight_g": 250,
 "calories": 400, "protein": 20, "fat": 15, "carbs": 45}
Якщо на фото кілька страв — назви їх через кому і порахуй разом.
Якщо на фото немає їжі, поверни {"is_food": false}."""

NUMBER_FIELDS = ("weight_g", "calories", "protein", "fat", "carbs")

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def _normalize(data) -> dict:
    """Перевіряє відповідь Gemini і приводить числа до цілих."""
    # Деякі моделі повертають список [{...}] замість {...} — беремо перший елемент
    if isinstance(data, list):
        if not data:
            return {"is_food": False}
        data = data[0]
    if not data.get("is_food"):
        return {"is_food": False}
    result = {"is_food": True, "dish": str(data.get("dish", "Невідома страва"))}
    for field in NUMBER_FIELDS:
        if field not in data:
            raise ValueError(f"Gemini не повернув поле {field}")
        result[field] = round(float(data[field]))
    return result


async def analyze_food(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    last_error = None
    for model in MODELS:
        try:
            response = await asyncio.wait_for(
                _get_client().aio.models.generate_content(
                    model=model,
                    contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type), PROMPT],
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                ),
                timeout=TIMEOUT_SECONDS,
            )
            return _normalize(json.loads(response.text))
        except asyncio.TimeoutError:
            print(f"  {model}: не відповіла за {TIMEOUT_SECONDS} с, пробую наступну модель", flush=True)
            last_error = TimeoutError(f"{model} не відповіла вчасно")
        except errors.APIError as e:
            last_error = e
            if e.code in (429, 500, 503):
                print(f"  {model}: помилка {e.code}, пробую наступну модель", flush=True)
                continue
            raise
    raise last_error