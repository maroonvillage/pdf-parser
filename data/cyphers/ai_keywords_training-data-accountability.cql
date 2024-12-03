// Create the Training Data Accountability node
CREATE (:Keyword {name: 'Training Data Accountability'});

// Add relationships between Training Data Accountability and other nodes
MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (accountability)-[:ENFORCES]->(ethics);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (transparency:Keyword {name: 'Transparency'})
CREATE (accountability)-[:PROMOTES]->(transparency);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (general_account:Keyword {name: 'Accountability'})
CREATE (accountability)-[:REQUIRES]->(general_account);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (bias_mitigation:Keyword {name: 'Bias Mitigation'})
CREATE (accountability)-[:SUPPORTS]->(bias_mitigation);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (fairness:Keyword {name: 'Fairness'})
CREATE (accountability)-[:ENSURES]->(fairness);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (accountability)-[:REQUIRES]->(privacy);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (protection:Keyword {name: 'Data Protection'})
CREATE (accountability)-[:SUPPORTS]->(protection);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (accountability)-[:ALIGNS_WITH]->(regulatory);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (accountability)-[:REQUIRED_BY]->(gdpr);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (accountability)-[:DOCUMENTS]->(audit);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (explain:Keyword {name: 'Explainability'})
CREATE (accountability)-[:ENHANCES]->(explain);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (robust:Keyword {name: 'Robustness'})
CREATE (accountability)-[:SUPPORTS]->(robust);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (security:Keyword {name: 'Security'})
CREATE (accountability)-[:REQUIRES]->(security);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (accountability)-[:REQUIRES]->(oversight);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (governance:Keyword {name: 'Data Governance'})
CREATE (accountability)-[:INTEGRATES_WITH]->(governance);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (risk:Keyword {name: 'Risk Management'})
CREATE (accountability)-[:MITIGATES]->(risk);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (accountability)-[:SUPPORTS]->(ethical);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (algo_accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (accountability)-[:ENHANCES]->(algo_accountability);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (accountability)-[:SUPPORTS]->(monitoring);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (accountability)-[:INTEGRATES_WITH]->(compliance);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (accountability)-[:INFORMS]->(engagement);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (responsible:Keyword {name: 'Responsible AI'})
CREATE (accountability)-[:SUPPORTS]->(responsible);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (trust:Keyword {name: 'Trustworthiness'})
CREATE (accountability)-[:BUILDS]->(trust);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (consent:Keyword {name: 'Informed Consent'})
CREATE (accountability)-[:REQUIRES]->(consent);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (impact:Keyword {name: 'Impact Assessment'})
CREATE (accountability)-[:INTEGRATES_WITH]->(impact);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (diversity:Keyword {name: 'Diversity in AI'})
CREATE (accountability)-[:PROMOTES]->(diversity);

MATCH (accountability:Keyword {name: 'Training Data Accountability'}), (vendor:Keyword
