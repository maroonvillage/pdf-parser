// Create the GDPR node
CREATE (:Keyword {name: 'GDPR (General Data Protection Regulation)'});

// Add relationships between GDPR and other nodes
MATCH (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (gdpr)-[:INCORPORATES]->(ethics);

MATCH (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'}), (transparency:Keyword {name: 'Transparency'})
CREATE (gdpr)-[:MANDATES]->(transparency);

MATCH (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'}), (accountability:Keyword {name: 'Accountability'})
CREATE (gdpr)-[:ENFORCES]->(accountability);

MATCH (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (gdpr)-[:ALIGNS_WITH]->(bias);

MATCH (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'}), (fairness:Keyword {name: 'Fairness'})
CREATE (gdpr)-[:REQUIRES]->(fairness);

MATCH (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (gdpr)-[:PROTECTS]->(privacy);

MATCH (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'}), (protection:Keyword {name: 'Data Protection'})
CREATE (gdpr)-[:SETS_STANDARDS_FOR]->(protection);

MATCH (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (gdpr)-[:IS_A]->(regulatory);
