// Create the Informed Consent node
CREATE (:Keyword {name: 'Informed Consent'});

// Add relationships between Informed Consent and other nodes
MATCH (consent:Keyword {name: 'Informed Consent'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (consent)-[:ENSURES]->(ethics);

MATCH (consent:Keyword {name: 'Informed Consent'}), (transparency:Keyword {name: 'Transparency'})
CREATE (consent)-[:REQUIRES]->(transparency);

MATCH (consent:Keyword {name: 'Informed Consent'}), (account:Keyword {name: 'Accountability'})
CREATE (consent)-[:ENFORCED_BY]->(account);

MATCH (consent:Keyword {name: 'Informed Consent'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (consent)-[:SUPPORTS]->(bias);

MATCH (consent:Keyword {name: 'Informed Consent'}), (fairness:Keyword {name: 'Fairness'})
CREATE (consent)-[:REINFORCES]->(fairness);

MATCH (consent:Keyword {name: 'Informed Consent'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (consent)-[:UPHOLDS]->(privacy);

MATCH (consent:Keyword {name: 'Informed Consent'}), (protection:Keyword {name: 'Data Protection'})
CREATE (consent)-[:REQUIRES]->(protection);

MATCH (consent:Keyword {name: 'Informed Consent'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (consent)-[:ESSENTIAL_FOR]->(regulatory);

MATCH (consent:Keyword {name: 'Informed Consent'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (consent)-[:MANDATED_BY]->(gdpr);

MATCH (consent:Keyword {name: 'Informed Consent'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (consent)-[:DOCUMENTED_BY]->(audit);

MATCH (consent:Keyword {name: 'Informed Consent'}), (explain:Keyword {name: 'Explainability'})
CREATE (consent)-[:SUPPORTED_BY]->(explain);

MATCH (consent:Keyword {name: 'Informed Consent'}), (robust:Keyword {name: 'Robustness'})
CREATE (consent)-[:REQUIRES]->(robust);

MATCH (consent:Keyword {name: 'Informed Consent'}), (security:Keyword {name: 'Security'})
CREATE (consent)-[:PROTECTED_BY]->(security);

MATCH (consent:Keyword {name: 'Informed Consent'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (consent)-[:ENSURED_BY]->(oversight);

MATCH (consent:Keyword {name: 'Informed Consent'}), (governance:Keyword {name: 'Data Governance'})
CREATE (consent)-[:SUPPORTED_BY]->(governance);

MATCH (consent:Keyword {name: 'Informed Consent'}), (risk:Keyword {name: 'Risk Management'})
CREATE (consent)-[:MITIGATES]->(risk);

MATCH (consent:Keyword {name: 'Informed Consent'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (consent)-[:ALIGNS_WITH]->(ethical);

MATCH (consent:Keyword {name: 'Informed Consent'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (consent)-[:UPHELD_BY]->(accountability);

MATCH (consent:Keyword {name: 'Informed Consent'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (consent)-[:ENSURED_BY]->(monitoring);

MATCH (consent:Keyword {name: 'Informed Consent'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (consent)-[:DEFINED_BY]->(compliance);

MATCH (consent:Keyword {name: 'Informed Consent'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (consent)-[:SUPPORTED_BY]->(engagement);

MATCH (consent:Keyword {name: 'Informed Consent'}), (responsible:Keyword {name: 'Responsible AI'})
CREATE (consent)-[:EMPHASIZED_BY]->(responsible);

MATCH (consent:Keyword {name: 'Informed Consent'}), (trust:Keyword {name: 'Trustworthiness'})
CREATE (consent)-[:BUILDS]->(trust);
