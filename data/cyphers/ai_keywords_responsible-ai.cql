// Create the Responsible AI node
CREATE (:Keyword {name: 'Responsible AI'});

// Add relationships between Responsible AI and other nodes
MATCH (responsible:Keyword {name: 'Responsible AI'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (responsible)-[:OPERATIONALIZES]->(ethics);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (transparency:Keyword {name: 'Transparency'})
CREATE (responsible)-[:PRIORITIZES]->(transparency);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (account:Keyword {name: 'Accountability'})
CREATE (responsible)-[:ENSURES]->(account);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (responsible)-[:INCLUDES]->(bias);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (fairness:Keyword {name: 'Fairness'})
CREATE (responsible)-[:ENSURES]->(fairness);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (responsible)-[:INCORPORATES]->(privacy);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (protection:Keyword {name: 'Data Protection'})
CREATE (responsible)-[:ENFORCES]->(protection);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (responsible)-[:ALIGNS_WITH]->(regulatory);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (responsible)-[:COMPLIES_WITH]->(gdpr);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (responsible)-[:USES]->(audit);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (explain:Keyword {name: 'Explainability'})
CREATE (responsible)-[:EMPHASIZES]->(explain);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (robust:Keyword {name: 'Robustness'})
CREATE (responsible)-[:PROMOTES]->(robust);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (security:Keyword {name: 'Security'})
CREATE (responsible)-[:ENFORCES]->(security);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (responsible)-[:INTEGRATES]->(oversight);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (governance:Keyword {name: 'Data Governance'})
CREATE (responsible)-[:REQUIRES]->(governance);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (risk:Keyword {name: 'Risk Management'})
CREATE (responsible)-[:INTEGRATES]->(risk);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (responsible)-[:ALIGN_WITH]->(ethical);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (responsible)-[:ENFORCES]->(accountability);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (responsible)-[:REQUIRES]->(monitoring);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (responsible)-[:ALIGNS_WITH]->(compliance);

MATCH (responsible:Keyword {name: 'Responsible AI'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (responsible)-[:ENHANCES]->(engagement);
