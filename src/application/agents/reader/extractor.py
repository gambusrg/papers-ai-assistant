from typing import Dict

from pymupdf import Document


def extract(doc: Document) -> Dict:
    """Extract all the data from the pdf

    Args:
        doc (Document): PyMuPDF document object

    Returns:
        Dict: extracted title, headers, content and pages
    """
    headers = []
    text = ""

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        text += page.get_text()
        for block in blocks:
            if block.get("type") == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] >= 11:
                            headers.append(span["text"])

    return {
        "title": doc.metadata.get("title", ""),
        "headers": headers,
        "content": text,
        "pages": len(doc),
    }
