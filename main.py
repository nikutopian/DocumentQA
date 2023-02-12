import os

from document_parser import DocumentParser
from openai_utils import OpenAIWrapper
from snippet_indexer import SnippetEmbeddingIndexer

filepath = '/Users/nikhilramesh/Downloads/Zomato IPO note (1).pdf'
name = os.path.basename(filepath)

parser = DocumentParser(name, filepath)
snippets = parser.get_snippets()
indexer = SnippetEmbeddingIndexer(name, snippets)
indexer.create_index()
wrapper = OpenAIWrapper()

while True:
    search_query = input("Enter a query to search the document: ")
    snippets, distances = indexer.search_index(search_query)
    for snippet, distance in zip(snippets, distances):
        print(f"Page Number: {snippet.page_index} :: Similarity Distance: {distance:.2f}")
        # print(snippet.text)

    print("-"*100)
    print(wrapper.custom_gpt_call_code(snippets[0].text, search_query))
    print("-"*100)
    print()

