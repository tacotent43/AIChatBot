from typing import List

from config import BASE_SYSTEM_PROMPT, STYLES, TELEGRAM_WRAPPER_INSTRUCTION, TG_MESSAGE_LIMIT


def build_system_prompt(style: str) -> str:
    style_instr = STYLES.get(style, STYLES["default"])
    return "\n\n".join(
        [
            BASE_SYSTEM_PROMPT,
            f"Response style: {style_instr}",
            TELEGRAM_WRAPPER_INSTRUCTION,
        ]
    )


def split_text_for_telegram(text: str, limit: int = TG_MESSAGE_LIMIT) -> List[str]:
    if len(text) <= limit:
        return [text]
    parts, start = [], 0
    while start < len(text):
        end = start + limit
        if end < len(text):
            nl = text.rfind("\n", start, end)
        if nl > start:
            end = nl + 1
        parts.append(text[start:end])
        start = end
    return parts
