# AIChatBot

AIChatBot is an asynchronous Telegram bot powered by modern LLMs, supporting OpenAI and LM-Studio models.  
It provides a conversational interface with context memory, flexible response styles, and safe handling of long messages.

---

## Features

- Context-aware conversations with each user, stored in a lightweight SQLite database.
- Automatic handling of long messages with safe MarkdownV2 formatting.
- Supports multiple response styles and prompt modifications.
- Regeneration of responses upon user request.
- Compatible with OpenAI API and LM-Studio local instances.
- Fully asynchronous implementation using `aiogram` for high performance.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tacotent43/AIChatBot.git
cd AIChatBot
```

2. Install dependencies (using uv):

```bash
uv sync
```

3. Create a .env file based on .env.example:

```bash
cp .env.example .env
```

## Configuration

All configuration values are loaded from the environment variables via config.py.

## How it Works

- Receiving Messages: The bot receives messages from Telegram via aiogram.
- Context Management: User conversation history is stored in SQLite.
- Generating Responses: Requests are sent to the chosen LLM (via OpenAI API) with optional prompt augmentation and style.
- Sending Responses: Responses are safely split into multiple messages if too long and MarkdownV2 is escaped to prevent Telegram errors.
- Style and Regeneration: Users can switch response styles or request regeneration for improved outputs.
