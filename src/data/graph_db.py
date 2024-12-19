from neo4j import GraphDatabase


class GraphDB:
    def __init__(self, db_name, uri, user_id, auth_key):
        # URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
        self._URI = uri
        self._user_id = user_id
        self._auth_key = auth_key
        #self._AUTH = (user_id, auth_key)
        self._db_name = db_name
        
      
    def get_keyworsds_graphdb(self):

        # Query the graph
        query = """
        MATCH (k:Keyword)
        RETURN k.name AS Keyword
        """
        
        with GraphDatabase.driver(self._URI, auth=(self._user_id, self._auth_key)) as driver:
            driver.verify_connectivity()
    
            records, summary, keys = driver.execute_query(
                query,
                database_=self._db_name
            )

        return records