from typing import Any, Dict, List, Tuple
from snippet import Snippet
import os
import nmslib
from openai.embeddings_utils import get_embedding

BASE_PATH = os.path.expanduser("~/data/indexes/")

class SnippetEmbeddingIndexer:
    def __init__(self, name: str, snippets: List[Snippet]) -> None:
        self.text_embeddings = []
        self.snippets = snippets
        if not os.path.exists(BASE_PATH):
            os.makedirs(BASE_PATH)
        self.index_path = os.path.join(BASE_PATH, name)

    def get_embedding(self, text: str):
        return get_embedding(text, engine='text-embedding-ada-002')

    def __compute_embeddings(self):
        print("Computing Embeddings on all Snippets ...")
        if self.text_embeddings:
            return
        for snippet in self.snippets:
            text_embedding = self.get_embedding(snippet.text)
            self.text_embeddings.append(text_embedding)
    
    def create_index(self):
        print("Creating Nearest Neighbor Search Index on all Function Embeddings ...")
        self.index = nmslib.init(method='hnsw', space='cosinesimil')
        if os.path.exists(self.index_path):
            self.index.loadIndex(self.index_path, load_data=True)
        else:
            self.__compute_embeddings()
            self.index.addDataPointBatch(self.text_embeddings)
            self.index.createIndex({'post': 2}, print_progress=True)
            self.index.saveIndex(self.index_path, save_data=True)

    def search_index(self, query: str, num_neighbors: int = 3) -> Tuple[List[Dict[str, Any]], List[float]]:
        query_embedding = self.get_embedding(query)
        ids, distances = self.index.knnQuery(query_embedding, k=num_neighbors)
        snippet_neighbors = [
            self.snippets[i] for i in ids
        ]
        return snippet_neighbors, distances




    