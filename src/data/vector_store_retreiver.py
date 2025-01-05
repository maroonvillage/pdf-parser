from typing import List, Dict, Any
from langchain_core.retrievers import  BaseRetriever
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.schema import Document
from langchain_core.embeddings import Embeddings
from langchain_community.llms import Ollama
from pydantic import BaseModel

from sentence_transformers import SentenceTransformer
import pinecone

class SentenceTransformerEmbeddings(Embeddings):
    """
    A Custom class that implements the Embeddings interface from langchain
    using a Sentence Transformer model from HuggingFace.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str) -> List[float]:
         """Embed a single query."""
         return self.model.encode(text).tolist()


class VectorStoreRetriever(BaseRetriever, BaseModel):
    """A custom retriever to return data from the vector store"""
    def __init__(self, index: pinecone.index.Index, embeddings: Embeddings, top_k: int = 5):
       super().__init__()
       self._index = index
       self._top_k = top_k
       self._embeddings = embeddings
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Get documents relevant for a query."""
        # Search for a query within the document sections
        query_embedding = self.embeddings.embed_query(query)
        search_results = self.index.query(
              vector=query_embedding,
              top_k=self.top_k,
              include_values=True
         )
        
        docs = [Document(
              page_content=match['id'],
              metadata={"score":match['score']}
            ) for match in search_results.matches ]

        return docs