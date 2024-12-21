import pinecone
from pinecone import Pinecone, ServerlessSpec
from datetime import datetime
from sentence_transformers import SentenceTransformer

class PineConeVectorDB:
    def __init__(self, api_key, prefix):
        
        self._api_key = api_key
        # Get the current date and time
        now = datetime.now()
        # Format the date and time as a string (e.g., '2023-04-06_14-30-00')
        timestamp = now.strftime("%Y%m%d%H%M%S")

        index_name = f"{prefix.replace("_","").lower()}-{timestamp}"
        self._index_name = index_name
        
        self._index = None

    @property
    def pineconedb(self):
        return self._pineconedb

    @pineconedb.setter 
    def pineconedb(self, value): 
        """Setter method for name""" 
        if not value: 
            raise ValueError("DB cannot be empty") 
        self._pineconedb = value
    
    
    @property
    def api_key(self):
        return self._api_key
    
    
    @api_key.setter 
    def api_key(self, value): 
        """Setter method for name""" 
        if not value: 
            raise ValueError("API Key cannot be empty") 
        self._api_key = value

    
    @property 
    def index_name(self): 
        """Getter method for _index_name """ 
        return self._index_name

    @property
    def index(self):
        return self._index
    
    
    def add_embeddings_to_pinecone_index(self, embeddings, dim=384, metric='euclidean',cloud='aws',region='us-east-1'):

        if(not self.api_key):
            raise ValueError("API Key name cannot be empty")
        

        if(not self.index_name):
            raise ValueError("Index name cannot be empty")
        
        self.pineconedb = Pinecone(
            api_key=self.api_key
        )
        
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
    
    
def output_search_results_to_file(prefix, keyword, search_results, sections):
    # Example structure for storing sections and subsections
    document_json = {
        "title": f"Extracted document for keyword {keyword}",
        "sections": []
    }

    if(search_results):
        # Append sections to the JSON object
        for match in search_results['matches']:
            section_id = int(match['id'])
            document_json["sections"].append({
                "section_id": section_id,
                "content": sections[section_id]
            })
    
        # Remove spaces and set all characters to lower case 
        modified_string = keyword.replace(" ", "").lower()
        file_name = f'{prefix}_query_results_{modified_string}.json'
        
        
        # Save the structured data to a JSON file
        with open(os.path.join('data/output', file_name), 'w') as json_file:
            json.dump(document_json, json_file, indent=2)
        
        print(f"{os.path.join('data/output', file_name)} saved to JSON!")
    else:
        print("No search results!")