import pinecone
from pinecone import Pinecone, ServerlessSpec
from datetime import datetime
from sentence_transformers import SentenceTransformer

class PineConeVectorDB:
    def __init__(self, api_key, prefix):
        
        self.pineconedb = Pinecone(
            api_key=api_key
        )
        # Get the current date and time
        now = datetime.now()
        # Format the date and time as a string (e.g., '2023-04-06_14-30-00')
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        index_name = f"{prefix}_{timestamp}"
        self._index_name = index_name


    @property 
    def index_name(self): 
        """Getter method for _index_name """ 
        return self._index_name

    @classmethod 
    def add_embeddings_to_pinecone_index(self, embeddings, dim=384, metric='euclidean',cloud='aws',region='us-east-1'):

        if(not self.index_name):
            raise ValueError("Index name cannot be empty")
        
        # Now do stuff
        if self.index_name not in self.pineconedb.list_indexes().names():
            self.pineconedb.create_index(
                name=self.index_name, 
                dimension=dim, 
                metric=metric,
                spec=ServerlessSpec(
                    cloud=cloud,
                    region=region
                )
            )

        # Connect to the index
        self._index = self.pineconedb.Index(self.index_name)

        # Upload section embeddings
        for i, embedding in enumerate(embeddings):
            self.index.upsert([(str(i), embedding)])

@classmethod            
def get_vectordb_search_results(self, query, model_name='sentence-transformers/all-MiniLM-L6-v2'):

    model = SentenceTransformer(model_name)
    # Search for a query within the document sections
    query_embedding = model.encode([query])
    #print(query_embedding[0])
    query_embedding_list = query_embedding[0].tolist()
    
    # Search the vector database
    #search_results = index.query(vector=query_embedding[0], top_k=5)
    search_results = self._index.query(
        
        vector=query_embedding_list,
        top_k=5,
        include_values=True
    )

    return search_results