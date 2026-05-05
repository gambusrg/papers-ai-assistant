from abc import ABC, abstractmethod

from src.domain.models import RawPaper


class Reader(ABC):
    """
    Defines the interface for strategy

    Args:
        ABC (_type_): _description_
    """

    @abstractmethod
    def read(self, source: str) -> RawPaper:
        pass
