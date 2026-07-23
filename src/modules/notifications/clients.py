from abc import ABC, abstractmethod

class INotificationChannelAdapter(ABC):
    """
    Strategy Contract for individual notification channels (OCP).
    """

    @abstractmethod
    async def send(self, recipient: str, title: str, content: str) -> None:
        pass