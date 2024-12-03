// Create the Model Monitoring node
CREATE (:Keyword {name: 'Model Monitoring'});

// Add relationships between Model Monitoring and other nodes
MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (monitoring)-[:ENSURES]->(ethics);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (transparency:Keyword {name: 'Transparency'})
CREATE (monitoring)-[:PROMOTES]->(transparency);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (account:Keyword {name: 'Accountability'})
CREATE (monitoring)-[:ESTABLISHES]->(account);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (monitoring)-[:DETECTS_AND_ADDRESSES]->(bias);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (fairness:Keyword {name: 'Fairness'})
CREATE (monitoring)-[:ENSURES]->(fairness);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (monitoring)-[:PROTECTS]->(privacy);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (protection:Keyword {name: 'Data Protection'})
CREATE (monitoring)-[:ENFORCES]->(protection);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (monitoring)-[:ESSENTIAL_FOR]->(regulatory);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (monitoring)-[:MANDATED_BY]->(gdpr);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (monitoring)-[:GENERATES]->(audit);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (explain:Keyword {name: 'Explainability'})
CREATE (monitoring)-[:SUPPORTS]->(explain);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (robust:Keyword {name: 'Robustness'})
CREATE (monitoring)-[:ENHANCES]->(robust);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (security:Keyword {name: 'Security'})
CREATE (monitoring)-[:DETECTS_RISKS]->(security);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (monitoring)-[:SUPPORTS]->(oversight);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (governance:Keyword {name: 'Data Governance'})
CREATE (monitoring)-[:RELIES_ON]->(governance);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (risk:Keyword {name: 'Risk Management'})
CREATE (monitoring)-[:INTEGRAL_TO]->(risk);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (monitoring)-[:SUPPORTS]->(ethical);

MATCH (monitoring:Keyword {name: 'Model Monitoring'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (monitoring)-[:ENFORCES]->(accountability);
