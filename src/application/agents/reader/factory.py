from src.application.agents.reader.strategies.base import Reader
from src.application.agents.reader.strategies.url_reader import URLReader
from src.application.agents.reader.strategies.pdf_reader import FileReader


class ReaderFactory:
    @staticmethod
    def create_strategy(source: str) -> Reader:
        """Selects the appropriate reader strategy based on the source.

        Args:
            source (str): URL (http/https) or local file path.

        Returns:
            Reader: URLReader for URLs, FileReader for local paths.
        """
        if source.startswith("http"):
            return URLReader()
        else:
            return FileReader()
