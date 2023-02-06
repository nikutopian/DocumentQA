class Snippet:
    def __init__(self, text: str, source: str, page_index: int = 0) -> None:
        self.text = text
        self.source = source
        self.page_index = page_index
        self.snippet_length = len(text)
