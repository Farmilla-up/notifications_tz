import logging
logger = logging.getLogger(__name__)


class NotificationService:
    """Оркестратор уведомлений, пробует отправку через несколько каналов."""
    def __init__(self, notifiers: list):
        self.notifiers = notifiers

    def notify(self, message, **kwargs):
        """
               Отправляет сообщение через каждый канал по очереди до успеха.

               Args:
                   message (str): Текст сообщения.
                   **kwargs: Параметры для конкретных нотификаторов (например, chat_id, phone, email).

               Returns:
                   dict: Информация о доставке, пример:
                       {"delivered": True, "channel": "SMSNotifier", "details": {...}} или
                       {"delivered": False, "error": "Все каналы недоступны"}
               """
        for notifier in self.notifiers:
            try:
                result = notifier.send_message(message, **kwargs)
                print(result, notifier.__class__.__name__)
                if result.get("success"):
                    return {
                        "delivered" : True,
                        "channel" : notifier.__class__.__name__,
                        "details" : result
                    }
            except Exception as e:
                logger.warning(f"{notifier.__class__.__name__} failed: {e}")
                continue

        else:
            return {"delivered": False, "error": "Все каналы недоступны"}