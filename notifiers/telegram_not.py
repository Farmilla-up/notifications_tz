from .base import Notifier
import requests
from decouple import config

class TelegramNotifier(Notifier):
    """Отправка сообщений через Telegram Bot API."""
    def __init__(self, **kwargs):
        try:
            self.chat_id = kwargs['chat_id']
            self.token = config('TELEGRAM_TOKEN')

        except KeyError as e:
            raise ValueError(f'Не указан ключ для "{e.args[0]}" в {self.__class__.__name__}')

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        try:
            response = requests.post(url, data=payload, timeout=5)
            response.raise_for_status()
            result = response.json()
            if result.get("ok"):
                return {"success": True, "details": "Сообщение отправлено"}
            else:
                return {"success": False, "error": result.get("description", "Неизвестная ошибка")}
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}