import pinecone
from pinecone import Pinecone, ServerlessSpec
from datetime import datetime
from sentence_transformers import SentenceTransformer
import logging
import os
import json
import numpy as np
from typing import List, Dict, Any
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain
#from langchain_pinecone import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings

from data.vector_store_retreiver import VectorStoreRetriever, SentenceTransformerEmbeddings
from utilities.file_util import generate_filename


class PineConeVectorDB:
    """
    A class to interact with Pinecone vector database.
    """
    def __init__(self, api_key: str, prefix: str):
        """
        Initializes the PineconeVectorDB with API key and a prefix.

        Parameters:
            api_key (str): The Pinecone API key.
            prefix (str): A prefix to use for the index name.
        """
        self._api_key = api_key
         # Get the current date and time
        now = datetime.now()
        # Format the date and time as a string (e.g., '2023-04-06_14-30-00')
        timestamp = now.strftime("%Y%m%d%H%M%S")

        self._index_name = f"{prefix.replace('_','').lower()}{timestamp}"
        self._index = None
        self._pineconedb = Pinecone(api_key=self._api_key)
        self._model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self._log = logging.getLogger(__name__)
    
    @property
    def api_key(self) -> str:
        """Getter method for the API Key"""
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str) -> None:
         """Setter method for API Key"""
         if not value:
            self._log.error("API Key cannot be empty")
            raise ValueError("API Key cannot be empty")
         self._api_key = value


    @property 
    def index_name(self) -> str:
        """Getter method for the Index Name"""
        return self._index_name

    @property
    def index(self) -> pinecone.index.Index:
         """Getter method for the Index"""
         if not self._index:
              self._log.error("Index has not been initialized. Please call `add_embeddings_to_pinecone_index` first.")
              raise ValueError("Index has not been initialized. Please call `add_embeddings_to_pinecone_index` first.")
         return self._index
    
    
    def add_embeddings_to_pinecone_index(self, embeddings: np.ndarray, dim: int = 384, metric: str = 'euclidean',cloud: str = 'aws',region: str = 'us-east-1') -> None:
       """
        Adds embeddings to a Pinecone index.

        Parameters:
            embeddings (List[List[float]]): A list of embeddings (list of list of floats).
            dim (int): The dimension of the embeddings.
            metric (str): The distance metric to use for the index (e.g., 'euclidean', 'cosine').
            cloud (str): The cloud provider for the Pinecone index.
            region (str): The region where the index is located.

        Raises:
             ValueError: If the API key or index name is empty, or if the index has already been initialized.
        """
       if not self.api_key:
           self.log.error("API Key name cannot be empty")
           raise ValueError("API Key name cannot be empty")

       if not self.index_name:
           self._log.error("Index name cannot be empty")
           raise ValueError("Index name cannot be empty")
       
       if self._index:
            self._log.error(f"Index with name {self.index_name} has been initialized. Cannot initialize again.")
            raise ValueError(f"Index with name {self.index_name} has been initialized. Cannot initialize again.")

       try:
            pc = Pinecone(api_key=self.api_key)
            #index_list = pc.list_indexes() #Call the method, and store the result in a variable
            
            #self._log.debug(f"Existing indexes: {index_list}")
            #if self.index_name not in index_list.names: #Access the names attribute using the `index_list` object
            #if pc.has_index(self.index_name) == False:
            self._index = _create_pinecone_index(pc, self._log, self.index_name, dim, metric, cloud, region)
            #if self.index_name not in self._pineconedb.list_indexes().names:
            #    self._index = _create_pinecone_index(self._pineconedb, self._log, self.index_name, dim, metric, cloud, region)
            #else:
            self._log.info(f"Index {self.index_name} already exists, using existing index.")
                
                # Connect to the index
            self._index = self._pineconedb.Index(self.index_name)
            _upsert_to_pinecone_index(self.index, embeddings)
            self._log.info(f"Successfully uploaded {len(embeddings)} embeddings to Pinecone index: {self.index_name}")
       except Exception as e:
                self._log.error(f"An error occurred when creating or upserting to Pinecone Index: {self.index_name}. Error: {e}")
                raise


    def get_vectordb_search_results(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Searches the Pinecone vector database for similar vectors to the query.

        Parameters:
            query (str): The query to search for.
            top_k (int): The number of results to return.
        Returns:
            Dict[str, Any]: The search results from Pinecone
        """
        
        try:
            self._log.info(f"Searching Pinecone index: {self.index_name} for query: {query}")
            query_embedding = self._model.encode([query]).tolist()
            self._log.debug(f"Query embedding: {query_embedding}")
            search_results = self.index.query(
                vector=query_embedding[0],
                top_k=top_k,
                include_values=True,
                include_metadata=True,
            )
            self._log.debug(f"Search results: {search_results}")
            return search_results
        except Exception as e:
           self._log.error(f"An error occurred while searching Pinecone index: {self.index_name} for query: {query}. Error: {e}")
           return {}

    def get_vectordb_search_results_lc(self, local_model: str, query: str, top_k: int = 5) -> Dict[str, Any]:
            """
            Searches the Pinecone vector database for similar vectors to the query, using langchain.

                Parameters:
                query (str): The query to search for.
                top_k (int): The number of results to return.
                Returns:
                Dict[str, Any]: The search results from Pinecone
        """
            log = logging.getLogger(__name__)
            try:
                log.info(f"Searching Pinecone index: {self.index_name} for query: {query}")
                
                #Prompt Template
                prompt_template = """
                Rephrase the following keyword into a question that can be used to retrieve documents related to AI compliance: {keyword}.
                """
                prompt = PromptTemplate(
                    input_variables = ["keyword"],
                    template=prompt_template
                )
                
                #LLM Chain
                #TODO: Replace this with your preferred LLM setup, I have used an example for OpenAI
                # llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), temperature=0)
                # llm_chain = LLMChain(prompt=prompt, llm = llm)
                #TODO: remove this placeholder code when an actual model is used.
                # class MockLLM():
                #     def invoke(self,input):
                #         return input
                # llm = MockLLM() #Placeholder code
                llm = ChatOllama(model=local_model)
                llm_chain = LLMChain(prompt=prompt, llm = llm, output_parser=StrOutputParser())
                
                #Initialize Embeddings
                #embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
                embeddings = SentenceTransformerEmbeddings()
                
                #VectorStore
                #vectorstore = Pinecone(self._index, embeddings, "text")
                vectorstore = self._pineconedb
                #Retriever
                retriever = VectorStoreRetriever(self.index, embeddings, top_k=top_k) #Use a custom vectorstore
                
                #Chain using LLM and Vector store
                chain = (
                    {"keyword": RunnablePassthrough()} | llm_chain | retriever
                )
                
                results = chain.invoke(query)
                log.debug(f"Search results: {results}")
                return results
            except Exception as e:
                log.error(f"An error occurred while searching Pinecone index: {self.index_name} for query: {query}. Error: {e}")
            return {}
        
    def output_search_results_to_file(self, prefix: str, keyword: str, search_results: Dict[str, Any], sections: List[str]) -> None:
        """
        Outputs the search results from Pinecone to a JSON file.

        Parameters:
            prefix (str): A prefix for the filename.
            keyword (str): The keyword used for the search.
            search_results (Dict[str, Any]): The search results from Pinecone.
            sections (List[str]): A list of document sections.
        Returns:
            None
        """
        try:
            document_json = {
                "title": f"{keyword}",
                "sections": []
            }
            if search_results and search_results.get("matches"):
                for match in search_results['matches']:
                    section_id = int(match['id'])
                    document_json["sections"].append({
                         "section_id": section_id,
                         "content": sections[section_id],
                         "score": match['score']
                     })
                modified_string = keyword.replace(" ", "").lower()
                file_name = f'{prefix}_query_results_{modified_string}'
                file_name = generate_filename(file_name, extension='json')
                full_path = os.path.join('data/output/query_results', file_name)

                with open(full_path, 'w') as json_file:
                   json.dump(document_json, json_file, indent=2)
                self._log.info(f"Saved search results to file: {full_path}")
            else:
                self._log.warning(f"No search results found for keyword: {keyword}")
        except FileNotFoundError as e:
             self._log.error(f"FileNotFoundError: {e} when saving file.")
        except KeyError as e:
             self._log.error(f"KeyError: {e} when extracting the data.")
        except Exception as e:
             self._log.error(f"An unexpected error occurred: {e} when saving the results. Error: {e}")
             
             
def _create_pinecone_index(db, logger, index_name, dim: int = 384, metric: str = 'euclidean', cloud: str = 'aws', region: str = 'us-east-1') -> pinecone.index.Index:
     """Creates the pinecone index."""
     try:
         logger.info(f"Creating Pinecone index: {index_name}")
         index =  db.create_index(
             name=index_name, 
             dimension=dim, 
             metric=metric,
             spec=ServerlessSpec(
                 cloud=cloud,
                 region=region
             )
         )
         logger.debug(f"Successfully created Pinecone index: {index_name}")
         return index
     except Exception as e:
         logger.error(f"An error occurred when creating Pinecone Index: {index_name}. Error: {e}")
         raise
                  
def _upsert_to_pinecone_index(index, embeddings: List[List[float]]) -> None:
    """
    Upserts embeddings to a Pinecone index.

    Parameters:
        index (pinecone.index.Index): The Pinecone index.
        embeddings (List[List[float]]): A list of embeddings (list of list of floats).
    """
    try:
        vectors = []
        # Iterate over the float list with an index 
        for i, embedding in enumerate(embeddings): 
            # Create a dictionary for each float value
            vector = { "id": str(i), 
            "values": embedding.tolist()
            } 
            # Append the dictionary to the list
            vectors.append(vector)
            
        index.upsert(vectors)
            
        # i = 0
        # for embedding in embeddings:
        #     index.upsert((str(i), [embedding]))
        #     i+=1

    except Exception as e:
        raise Exception(f"An error occurred when upserting to Pinecone Index. Error: {e}")