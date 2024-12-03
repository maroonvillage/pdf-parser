// Create the Security node
CREATE (:Keyword {name: 'Security'});

// Add relationships between Security and other nodes
MATCH (security:Keyword {name: 'Security'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (security)-[:SUPPORTS]->(ethics);

MATCH (security:Keyword {name: 'Security'}), (transparency:Keyword {name: 'Transparency'})
CREATE (security)-[:PROTECTS]->(transparency);

MATCH (security:Keyword {name: 'Security'}), (accountability:Keyword {name: 'Accountability'})
CREATE (security)-[:ENFORCES]->(accountability);

MATCH (security:Keyword {name: 'Security'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (security)-[:SAFEGUARDS]->(bias);

MATCH (security:Keyword {name: 'Security'}), (fairness:Keyword {name: 'Fairness'})
CREATE (security)-[:ENSURES]->(fairness);

MATCH (security:Keyword {name: 'Security'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (security)-[:ENFORCES]->(privacy);

MATCH (security:Keyword {name: 'Security'}), (protection:Keyword {name: 'Data Protection'})
CREATE (security)-[:UNDERPINS]->(protection);

MATCH (security:Keyword {name: 'Security'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (security)-[:REQUIRED_FOR]->(regulatory);

MATCH (security:Keyword {name: 'Security'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (security)-[:MANDATED_BY]->(gdpr);

MATCH (security:Keyword {name: 'Security'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (security)-[:PROTECTS]->(audit);

MATCH (security:Keyword {name: 'Security'}), (explain:Keyword {name: 'Explainability'})
CREATE (security)-[:SAFEGUARDS]->(explain);

MATCH (security:Keyword {name: 'Security'}), (robust:Keyword {name: 'Robustness'})
CREATE (security)-[:ENHANCES]->(robust);
