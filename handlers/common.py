from aiogram import types
from aiogram.filters import Command

from config import STYLES
from database import DB


def setup_common_handlers(dp, db: DB):
    @dp.message(Command(commands=['start']))
    async def cmd_start(message: types.Message):
        await db.set_style(message.chat.id, 'default')
        await message.reply("Hello! I am your custom self-hosted AI-assistant. Use /style to choose style.")


    @dp.message(Command(commands=["style"]))
    async def cmd_style(message: types.Message):
        parts = message.text.split(maxsplit=1)
        args = parts[1].strip() if len(parts) > 1 else ""

        if not args:
            current = await db.get_style(message.chat.id)
            text = "Available styles:\n" + "\n".join(
                [f"- {k}: {v}" for k, v in STYLES.items()]
            )
            text += f"\n\nCurrent style: {current}\nType `/style style_name` to change current style."
            await message.reply(text)
            return

        style = args.split()[0]
        if style not in STYLES:
            await message.reply("Undefined style. Use /style to see the list of styles.")
            return

        await db.set_style(message.chat.id, style)
        await message.reply(f"Style changed to: {style}")

    @dp.message(Command(commands=['clear']))
    async def cmd_clear(message: types.Message):
        await db.clear_context(message.chat.id)
        await message.reply("Context cleared.")