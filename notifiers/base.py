from abc import ABC, abstractmethod

class Notifier(ABC):
    """Абстрактный класс для всех нотификаторов."""
    @abstractmethod
    def send_message(self, message, **kwargs):
        pass


