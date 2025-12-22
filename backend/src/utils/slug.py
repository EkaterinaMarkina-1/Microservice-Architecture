import re

CYRILLIC_MAP = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "i", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ы": "y", "э": "e", "ю": "yu", "я": "ya", "ь": "", "ъ": ""
}


def slugify(text: str) -> str:
    if not text:
        return ""

    # В нижний регистр
    text = text.lower()

    # Транслитерация кириллицы
    text = "".join(CYRILLIC_MAP.get(c, c) for c in text)

    # Заменяем всё, что не буквы или цифры, на дефис
    text = re.sub(r"[^a-z0-9]+", "-", text)

    text = re.sub(r"-{2,}", "-", text).strip("-")

    return text
