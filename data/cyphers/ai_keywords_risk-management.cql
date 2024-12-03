// Create the Risk Management node
CREATE (:Keyword {name: 'Risk Management'});

// Add relationships between Risk Management and other nodes
MATCH (risk:Keyword {name: 'Risk Management'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (risk)-[:SUPPORTS]->(ethics);

MATCH (risk:Keyword {name: 'Risk Management'}), (transparency:Keyword {name: 'Transparency'})
CREATE (risk)-[:REQUIRES]->(transparency);

MATCH (risk:Keyword {name: 'Risk Management'}), (accountability:Keyword {name: 'Accountability'})
CREATE (risk)-[:ESTABLISHES]->(accountability);

MATCH (risk:Keyword {name: 'Risk Management'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (risk)-[:INCLUDES]->(bias);

MATCH (risk:Keyword {name: 'Risk Management'}), (fairness:Keyword {name: 'Fairness'})
CREATE (risk)-[:ENSURES]->(fairness);

MATCH (risk:Keyword {name: 'Risk Management'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (risk)-[:ADDRESSES]->(privacy);

MATCH (risk:Keyword {name: 'Risk Management'}), (protection:Keyword {name: 'Data Protection'})
CREATE (risk)-[:ENSURES]->(protection);

MATCH (risk:Keyword {name: 'Risk Management'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (risk)-[:ESSENTIAL_FOR]->(regulatory);

MATCH (risk:Keyword {name: 'Risk Management'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (risk)-[:MANDATED_BY]->(gdpr);

MATCH (risk:Keyword {name: 'Risk Management'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (risk)-[:USES]->(audit);

MATCH (risk:Keyword {name: 'Risk Management'}), (explain:Keyword {name: 'Explainability'})
CREATE (risk)-[:DEPENDS_ON]->(explain);

MATCH (risk:Keyword {name: 'Risk Management'}), (robust:Keyword {name: 'Robustness'})
CREATE (risk)-[:ENHANCES]->(robust);

MATCH (risk:Keyword {name: 'Risk Management'}), (security:Keyword {name: 'Security'})
CREATE (risk)-[:ADDRESSES]->(security);

MATCH (risk:Keyword {name: 'Risk Management'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (risk)-[:REQUIRES]->(oversight);

MATCH (risk:Keyword {name: 'Risk Management'}), (governance:Keyword {name: 'Data Governance'})
CREATE (risk)-[:RELIES_ON]->(governance);
