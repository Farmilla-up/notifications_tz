from notifiers.email_not import SendMail
from notifiers.sms_not import SMSNotifier
from notifiers.telegram_not import TelegramNotifier
from service.notification_orchestrator import NotificationService
from config import email, subject, phone, chat_id

def main():

    email_notifier = SendMail(
        email= email,
        subject= subject,
    )

    sms_notifier = SMSNotifier(
        phone = phone,
    )

    tg_notifier = TelegramNotifier(
        chat_id= chat_id,
    )


    service = NotificationService([sms_notifier, tg_notifier, email_notifier])

    result = service.notify(
        message="Привет! Это тестовое сообщение 🚀",
    )

    print(result)


if __name__ == "__main__":
    main()
