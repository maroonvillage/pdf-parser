// Create the Audit Trails node
CREATE (:Keyword {name: 'Audit Trails'});

// Add relationships between Audit Trails and other nodes
MATCH (audit:Keyword {name: 'Audit Trails'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (audit)-[:SUPPORTS]->(ethics);

MATCH (audit:Keyword {name: 'Audit Trails'}), (transparency:Keyword {name: 'Transparency'})
CREATE (audit)-[:ENABLES]->(transparency);

MATCH (audit:Keyword {name: 'Audit Trails'}), (accountability:Keyword {name: 'Accountability'})
CREATE (audit)-[:ENSURES]->(accountability);

MATCH (audit:Keyword {name: 'Audit Trails'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (audit)-[:DOCUMENTS]->(bias);

MATCH (audit:Keyword {name: 'Audit Trails'}), (fairness:Keyword {name: 'Fairness'})
CREATE (audit)-[:EVALUATES]->(fairness);

MATCH (audit:Keyword {name: 'Audit Trails'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (audit)-[:TRACKS]->(privacy);

MATCH (audit:Keyword {name: 'Audit Trails'}), (protection:Keyword {name: 'Data Protection'})
CREATE (audit)-[:LOGS]->(protection);

MATCH (audit:Keyword {name: 'Audit Trails'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (audit)-[:DEMONSTRATES]->(regulatory);

MATCH (audit:Keyword {name: 'Audit Trails'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (audit)-[:REQUIRED_BY]->(gdpr);
