// Create the Human Oversight node
CREATE (:Keyword {name: 'Human Oversight'});

// Add relationships between Human Oversight and other nodes
MATCH (oversight:Keyword {name: 'Human Oversight'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (oversight)-[:ENSURES]->(ethics);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (transparency:Keyword {name: 'Transparency'})
CREATE (oversight)-[:REQUIRES]->(transparency);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (accountability:Keyword {name: 'Accountability'})
CREATE (oversight)-[:ESTABLISHES]->(accountability);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (oversight)-[:SUPPORTS]->(bias);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (fairness:Keyword {name: 'Fairness'})
CREATE (oversight)-[:ENSURES]->(fairness);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (oversight)-[:ENFORCES]->(privacy);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (protection:Keyword {name: 'Data Protection'})
CREATE (oversight)-[:GUARDS]->(protection);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (oversight)-[:REQUIRED_FOR]->(regulatory);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (oversight)-[:MANDATED_BY]->(gdpr);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (oversight)-[:USES]->(audit);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (explain:Keyword {name: 'Explainability'})
CREATE (oversight)-[:DEPENDS_ON]->(explain);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (robust:Keyword {name: 'Robustness'})
CREATE (oversight)-[:COMPLEMENTS]->(robust);

MATCH (oversight:Keyword {name: 'Human Oversight'}), (security:Keyword {name: 'Security'})
CREATE (oversight)-[:MONITORS]->(security);
