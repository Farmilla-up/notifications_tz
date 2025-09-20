from .base import Notifier
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail(Notifier):
    """
    Класс для отправки письма через SMTP.
    """

    def __init__(self, **kwargs):
        try:
            self.email_to = kwargs["email"]
            self.subject = kwargs["subject"]
            self.password = config('MAIL_APP_PASSWORD')
            self.smtp_server = config('SMTP_SERVER')
            self.email_from = config('EMAIL_FROM')
            self.port = 465
            self.server = None

        except KeyError as e:
            raise ValueError(f'Не указан ключ для "{e.args[0]}" в {self.__class__.__name__}')

    def send_message(self, message) -> dict:
        """
        Основной публичный метод: подключается, отправляет письмо и закрывает соединение.
        """
        try:
            self._connect()
            result = self._send(message)
        finally:
            self._close()
        return result

    def _connect(self):
        """
        Подключение к SMTP серверу.
        """
        try:
            self.server = smtplib.SMTP_SSL(self.smtp_server, self.port)
            self.server.login(self.email_from, self.password)
        except Exception as e:
            raise ConnectionError(f"Не удалось подключиться к SMTP: {e}")

    def _send(self, message: str) -> dict:
        """
        Отправка письма.
        """
        msg = MIMEMultipart()
        msg["From"] = self.email_from
        msg["To"] = self.email_to
        msg["Subject"] = self.subject
        msg.attach(MIMEText(message, "plain"))

        if not self.server:
            return {"success": False, "error": "Нет соединения с сервером"}

        try:
            self.server.sendmail(self.email_from, self.email_to, msg.as_string())
            return {"success": True, "details": f"Письмо отправлено на {self.email_to}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _close(self):
        """
        Закрытие SMTP соединения.
        """
        if self.server:
            try:
                self.server.quit()
            except Exception:
                pass
            finally:
                self.server = None

