import json
import os

from google import genai
from google.genai import types

# Якщо буде помилка 404 "model not found" — замініть на назву Flash-моделі з AI Studio
MODEL = "gemini-3.5-flash"

PROMPT = """Ти дієтолог. Визнач страву на фото, оціни її вагу і КБЖВ на всю порцію.
Відповідай ЛИШЕ JSON такого вигляду:
{"is_food": true, "dish": "назва українською", "weight_g": 250,
 "calories": 400, "protein": 20, "fat": 15, "carbs": 45}
Якщо на фото немає їжі, поверни {"is_food": false}."""

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


async def analyze_food(image_bytes: bytes) -> dict:
    response = await _get_client().aio.models.generate_content(
        model=MODEL,
        contents=[types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"), PROMPT],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return json.loads(response.text)