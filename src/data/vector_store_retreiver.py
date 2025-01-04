from typing import List, Dict, Any
from langchain_core.retrievers import  BaseRetriever
from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain.schema import Document



from sentence_transformers import SentenceTransformer
import pinecone


class VectorStoreRetriever(BaseRetriever):
    """A custom retriever to return data from the vector store"""
    def __init__(self, index: pinecone.index.Index, top_k: int = 5):
       self.index = index
       self.top_k = top_k
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Get documents relevant for a query."""
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        # Search for a query within the document sections
        query_embedding = model.encode([query])
        query_embedding_list = query_embedding[0].tolist()
        search_results = self.index.query(
              vector=query_embedding_list,
              top_k=self.top_k,
              include_values=True
         )
        
        docs = [Document(
              page_content=match['id'],
              metadata={"score":match['score']}
            ) for match in search_results.matches ]

        return docs