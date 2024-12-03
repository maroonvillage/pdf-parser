// Create the Data Governance node
CREATE (:Keyword {name: 'Data Governance'});

// Add relationships between Data Governance and other nodes
MATCH (governance:Keyword {name: 'Data Governance'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (governance)-[:ENFORCES]->(ethics);

MATCH (governance:Keyword {name: 'Data Governance'}), (transparency:Keyword {name: 'Transparency'})
CREATE (governance)-[:ENHANCES]->(transparency);

MATCH (governance:Keyword {name: 'Data Governance'}), (accountability:Keyword {name: 'Accountability'})
CREATE (governance)-[:ESTABLISHES]->(accountability);

MATCH (governance:Keyword {name: 'Data Governance'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (governance)-[:SUPPORTS]->(bias);

MATCH (governance:Keyword {name: 'Data Governance'}), (fairness:Keyword {name: 'Fairness'})
CREATE (governance)-[:ENSURES]->(fairness);

MATCH (governance:Keyword {name: 'Data Governance'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (governance)-[:SUPPORTS]->(privacy);

MATCH (governance:Keyword {name: 'Data Governance'}), (protection:Keyword {name: 'Data Protection'})
CREATE (governance)-[:ENSURES]->(protection);

MATCH (governance:Keyword {name: 'Data Governance'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (governance)-[:REQUIRED_FOR]->(regulatory);

MATCH (governance:Keyword {name: 'Data Governance'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (governance)-[:MANDATED_BY]->(gdpr);

MATCH (governance:Keyword {name: 'Data Governance'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (governance)-[:USES]->(audit);

MATCH (governance:Keyword {name: 'Data Governance'}), (explain:Keyword {name: 'Explainability'})
CREATE (governance)-[:SUPPORTS]->(explain);

MATCH (governance:Keyword {name: 'Data Governance'}), (robust:Keyword {name: 'Robustness'})
CREATE (governance)-[:ENHANCES]->(robust);

MATCH (governance:Keyword {name: 'Data Governance'}), (security:Keyword {name: 'Security'})
CREATE (governance)-[:ENFORCES]->(security);

MATCH (governance:Keyword {name: 'Data Governance'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (governance)-[:ENABLES]->(oversight);
