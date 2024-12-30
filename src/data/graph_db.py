from neo4j import GraphDatabase
import logging
from typing import List, Dict, Any

class GraphDB:
    """
    A class to interact with Neo4j graph database.
    """
    def __init__(self, db_name: str, uri: str, user_id: str, auth_key: str):
        """
        Initializes the GraphDB with database name, URI, user ID and auth key.

        Parameters:
            db_name (str): The database name.
            uri (str): The Neo4j connection URI.
            user_id (str): The user ID for Neo4j authentication.
            auth_key (str): The authentication key for Neo4j.
        """
        self._URI = uri
        self._user_id = user_id
        self._auth_key = auth_key
        self._db_name = db_name
        self.log = logging.getLogger(__name__)
    
    def get_keyworsds_graphdb(self) -> List[Dict[str, Any]]:
        """
        Retrieves keywords from the graph database.

        Returns:
            List[Dict[str, Any]]: A list of records from the graph database.
        """
        query = """
        MATCH (k:Keyword)
        RETURN k.name AS Keyword
        """
        try:
           self.log.info(f"Connecting to Neo4j database: {self._db_name} at {self._URI}")
           with GraphDatabase.driver(self._URI, auth=(self._user_id, self._auth_key)) as driver:
              self.log.debug("Successfully connected to Neo4j database.")
              #driver.verify_connectivity() #Removed connectivity verification for performance reasons.
              records, summary, keys = driver.execute_query(
                   query,
                   database_=self._db_name
               )
              self.log.info(f"Successfully retrieved {len(records)} records from Neo4j database: {self._db_name}")
              self.log.debug(f"Retrieved records: {records}")
              return records
        except Exception as e:
            self.log.error(f"An error occurred while retrieving keywords from Neo4j database: {self._db_name}. Error: {e}")
            return []