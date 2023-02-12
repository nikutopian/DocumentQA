from PyPDF2 import PdfReader
from snippet import Snippet
from typing import List

MAX_TEXT_LENGTH = 2000

class DocumentParser():
    def __init__(self) -> None:
        pass

    @staticmethod
    def split_text(text) -> List[str]:
        if len(text) > MAX_TEXT_LENGTH:
            return [text[i:i+MAX_TEXT_LENGTH] for i in range(0, len(text), MAX_TEXT_LENGTH)]

    @staticmethod
    def parse(document_path: str) -> List[Snippet]:
        reader = PdfReader(document_path)
        snippets = []
        for index, page in enumerate(reader.pages):
            page_text = page.extract_text()
            snippets.extend(
                [
                    Snippet(x, document_path, index)
                    for x in DocumentParser.split_text(page_text)
                ]
            )
        return snippets

