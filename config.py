import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_PATH = os.getenv("BOT_DB_PATH", "bot_contexts.db")
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


TG_MESSAGE_LIMIT = 4000
MAX_CONTEXT_MESSAGES = 12


BASE_SYSTEM_PROMPT = "You are a helpful assistant. Answer clearly and concisely."
TELEGRAM_WRAPPER_INSTRUCTION = "Format the assistant's reply so it looks good in Telegram: use short paragraphs, markdown/HTML formatting, and light emojis."


STYLES = {
    "default": "Neutral, helpful tone.",
    "friendly": "Warm and friendly, with casual phrasing and occasional emojis.",
    "formal": "Formal, concise, polite.",
    "technical": "Detailed technical explanations, include code examples where appropriate.",
}
