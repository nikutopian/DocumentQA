import os
import pickle
from typing import List

from PyPDF2 import PdfReader
from tqdm import tqdm

from snippet import Snippet

BASE_PATH = os.path.expanduser("~/data/parsed_documents/")
MAX_TEXT_LENGTH = 3000

class DocumentParser():
    def __init__(self, name: str, document_path: str) -> None:
        self.name = name
        self.document_path = document_path

        if not os.path.exists(BASE_PATH):
            os.makedirs(BASE_PATH)
        self.snippet_dump_path = os.path.join(BASE_PATH, os.path.splitext(name)[0] + '.pkl')
        self.snippets = []
        if os.path.exists(self.snippet_dump_path):
            self.snippets = self.__load_snippets(self.snippet_dump_path)
        
        
    def get_snippets(self) -> List[Snippet]:
        if not self.snippets:
            self.snippets = self.__parse_pdf()
        return self.snippets

    def __load_snippets(self, filepath: str) -> List[Snippet]:
        try:
            with open(filepath, "rb") as fin:
                snippets: List[Snippet] = pickle.load(fin)
        except Exception as ex:
            print(f"Exception while trying to read snippets dump")
            snippets = self.__parse_pdf()
            self.__dump_snippets(snippets, filepath)
        return snippets

    def __dump_snippets(self, snippets: List[Snippet], filepath: str):
        with open(filepath, "wb") as fout:
            pickle.dump(snippets, fout)
        return snippets

    @staticmethod
    def split_text(text) -> List[str]:
        if len(text) > MAX_TEXT_LENGTH:
            return [text[i:i+MAX_TEXT_LENGTH] for i in range(0, len(text) - 1, MAX_TEXT_LENGTH) if text[i:i+MAX_TEXT_LENGTH]]
        elif len(text) > 0:
            return [text]
        return []

    
    def __parse_pdf(self) -> List[Snippet]:
        print("Parsing PDF Document and extracting text...")
        reader = PdfReader(self.document_path)
        snippets = []
        for index, page in tqdm(enumerate(reader.pages)):
            page_text = page.extract_text()
            snippets.extend(
                [
                    Snippet(x, self.document_path, index+1)
                    for x in DocumentParser.split_text(page_text)
                ]
            )
        self.__dump_snippets(snippets, self.snippet_dump_path)
        return snippets

