import logging

logger = logging.getLogger("petstore")

# httpx пишет собственную строку на каждый запрос - она дублирует нашу, но без тела и времени.
logging.getLogger("httpx").setLevel(logging.WARNING)

# password сюда не добавлен намеренно: в тестах он генерируется Faker и секретом не является.
# Стоит добавить, если фреймворк будет направлен на стенд с настоящими учётными данными.
SECRET_KEYS = {"api_key", "token"}


def mask_secrets(data: dict) -> dict:
    masked = {}
    for key, value in data.items():
        if key in SECRET_KEYS:
            masked[key] = "***"
        else:
            masked[key] = value
    return masked
