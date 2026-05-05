import pymupdf

from src.application.agents.reader.extractor import extract
from src.application.agents.reader.strategies.base import Reader
from src.domain.models import RawPaper


class FileReader(Reader):
    """Implements strategy methods for local PDF file reader"""

    def read(self, source: str) -> RawPaper:
        """Reads a pdf from a local file path

        Args:
            source (str): local path to the PDF file

        Returns:
            RawPaper: Object of the read paper
        """
        doc = pymupdf.open(source)
        document = extract(doc=doc)
        return RawPaper.from_dict(document=document)
