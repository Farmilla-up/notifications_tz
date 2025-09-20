from abc import ABC

from notifiers.base import Notifier
from decouple import config
from twilio.rest import Client

class SMSNotifier(Notifier):
    """Отправка SMS через Twilio."""
    def __init__(self, **kwargs):
        try:
            self.phone_to = kwargs['phone']
            self.client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))
            self.phone_from = config('TWILIO_PHONE_NUMBER')

        except KeyError as e:
            raise ValueError(f'Не указан ключ для "{e.args[0]}" в {self.__class__.__name__}')

    def send_message(self, message):
        try:
            msg = self.client.messages.create(
                body= message,
                from_=self.phone_from,
                to=self.phone_to,
            )
            return {"success": True, "details": msg.sid}

        except Exception as e:
            return {"success": False, "error": str(e)}
