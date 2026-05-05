import pymupdf
import requests

from src.application.agents.reader.extractor import extract
from src.application.agents.reader.strategies.base import Reader
from src.domain.models import RawPaper


class URLReader(Reader):
    """Implements strategy methods for URL pdf reader

    Args:
        Reader (_type_): _description_
    """

    def read(self, source: str) -> RawPaper:
        """Reads a pdf from a given URL

        Args:
            soruce (str): url of the paper to be read

        Returns:
            RawPaper: Object of the read paper
        """
        r = requests.get(source)
        data = r.content
        doc = pymupdf.Document(stream=data)

        document = extract(doc=doc)

        return RawPaper.from_dict(document=document)
