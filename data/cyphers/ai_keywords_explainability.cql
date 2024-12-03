// Create the Explainability node
CREATE (:Keyword {name: 'Explainability'});

// Add relationships between Explainability and other nodes
MATCH (explain:Keyword {name: 'Explainability'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (explain)-[:SUPPORTS]->(ethics);

MATCH (explain:Keyword {name: 'Explainability'}), (transparency:Keyword {name: 'Transparency'})
CREATE (explain)-[:ENHANCES]->(transparency);

MATCH (explain:Keyword {name: 'Explainability'}), (accountability:Keyword {name: 'Accountability'})
CREATE (explain)-[:FACILITATES]->(accountability);

MATCH (explain:Keyword {name: 'Explainability'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (explain)-[:ENABLES]->(bias);

MATCH (explain:Keyword {name: 'Explainability'}), (fairness:Keyword {name: 'Fairness'})
CREATE (explain)-[:ENSURES]->(fairness);

MATCH (explain:Keyword {name: 'Explainability'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (explain)-[:MAKES_CLEAR]->(privacy);

MATCH (explain:Keyword {name: 'Explainability'}), (protection:Keyword {name: 'Data Protection'})
CREATE (explain)-[:CLARIFIES]->(protection);

MATCH (explain:Keyword {name: 'Explainability'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (explain)-[:REQUIRED_FOR]->(regulatory);

MATCH (explain:Keyword {name: 'Explainability'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (explain)-[:EMPHASIZED_BY]->(gdpr);

MATCH (explain:Keyword {name: 'Explainability'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (explain)-[:WORKS_WITH]->(audit);
