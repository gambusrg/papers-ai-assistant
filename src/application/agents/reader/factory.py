from src.application.agents.reader.strategies.base import Reader
from src.application.agents.reader.strategies.url_reader import URLReader
from src.application.agents.reader.strategies.pdf_reader import FileReader


class ReaderFactory:
    """
    Determines which factory create
    """

    @staticmethod
    def create_strategy(source: str) -> Reader:
        """
        Creates the strategy based on the source

        Args:
            source (_type_): _description_

        Returns:
            Reader: _description_
        """
        if source.startswith("http"):
            return URLReader()
        else:
            return FileReader()
