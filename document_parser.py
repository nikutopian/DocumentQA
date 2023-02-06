from PyPDF2 import PdfReader
from snippet import Snippet
from typing import List

class DocumentParser():
    def __init__(self) -> None:
        pass

    @staticmethod
    def parse(document_path: str) -> List[Snippet]:
        reader = PdfReader(document_path)
        snippets = []
        for index, page in enumerate(reader.pages):
            page_text = page.extract_text()
            snippets.append(Snippet(page_text, document_path, index))
        return snippets

