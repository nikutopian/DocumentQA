from document_parser import DocumentParser
from snippet import Snippet
from snippet_indexer import SnippetEmbeddingIndexer

snippets = DocumentParser.parse('/Users/nikhilramesh/Workspace/ML Papers/DeepBidirectionalLanguageKnowledge.pdf')
indexer = SnippetEmbeddingIndexer('pdf', snippets)
indexer.create_index()

while True:
    search_query = input("Enter a query to search the document: ")
    snippets, distances = indexer.search_index(search_query)
    print((snippets, distances))
    import pdb; pdb.set_trace()

