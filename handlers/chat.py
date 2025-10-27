from aiogram import Bot, types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MAX_CONTEXT_MESSAGES
from openai_client import call_openai_chat
from utils import build_system_prompt, split_text_for_telegram


async def build_messages_for_api(db, chat_id: int, user_message: str):
    style = await db.get_style(chat_id)
    messages = [{"role": "system", "content": build_system_prompt(style)}]
    recent = await db.get_recent_messages(chat_id, limit=MAX_CONTEXT_MESSAGES)
    messages += [{"role": r["role"], "content": r["content"]} for r in recent]
    messages.append({"role": "user", "content": user_message})
    return messages


def setup_chat_handlers(dp, bot: Bot, db):
    async def send_long_message(chat_id: int, text: str, reply_to_message_id=None):
        parts = split_text_for_telegram(text)
        sent = None
        for p in parts:
            sent = await bot.send_message(
                chat_id, p, reply_to_message_id=reply_to_message_id, parse_mode="Markdown"
            )
        return sent

    @dp.message()
    async def handle_message(message: types.Message):
        user_text = message.text or ""
        if not user_text.strip():
            return
        await db.add_message(message.chat.id, "user", user_text)
        msgs = await build_messages_for_api(db, message.chat.id, user_text)
        ai_response = await call_openai_chat(msgs)
        await db.add_message(message.chat.id, "assistant", ai_response)
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text="Regenerate", callback_data=f"regen:{message.message_id}"))
        sent = await send_long_message(
            message.chat.id, ai_response, reply_to_message_id=message.message_id
        )
        await bot.send_message(
            message.chat.id, "—", reply_to_message_id=sent.message_id, reply_markup=kb.as_markup()
        )

    @dp.callback_query(lambda c: c.data and c.data.startswith("regen:"))
    async def callback_regenerate(callback: types.CallbackQuery):
        await callback.answer()
        chat_id = callback.message.chat.id
        all_recent = await db.get_recent_messages(chat_id, limit=MAX_CONTEXT_MESSAGES)
        last_user = next((m["content"] for m in reversed(all_recent) if m["role"] == "user"), None)
        if not last_user:
            await callback.message.reply("Нет последнего запроса.")
            return
        msgs = await build_messages_for_api(db, chat_id, last_user)
        ai_response = await call_openai_chat(msgs, temperature=0.9)
        await db.add_message(chat_id, "assistant", ai_response)
        try:
            await callback.message.delete()
        except Exception:
            pass
        sent = await send_long_message(chat_id, ai_response)
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text="Regenerate", callback_data=f"regen:0"))
        await bot.send_message(
            chat_id, "—", reply_to_message_id=sent.message_id, reply_markup=kb.as_markup()
        )
