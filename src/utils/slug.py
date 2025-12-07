import re
import unicodedata


def slugify(text: str) -> str:
    """
    Преобразует строку в URL-friendly slug.
    Пример:
        "Микросервисная архитектура!" -> "mikroservisnaya-arkhitektura"
        "Hello World" -> "hello-world"
    """

    # Normalize unicode (убирает диакритику)
    text = unicodedata.normalize("NFKD", text)

    # Транслитерация кириллицы в латиницу
    text = text.encode("ascii", "ignore").decode("ascii")

    # в нижний регистр
    text = text.lower()

    # заменяем всё не-буквы/цифры на дефис
    text = re.sub(r"[^a-z0-9]+", "-", text)

    # убираем дефисы по краям и двойные
    text = re.sub(r"-{2,}", "-", text).strip("-")

    return text
