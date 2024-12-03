// Create the Incident Response node
CREATE (:Keyword {name: 'Incident Response'});

// Add relationships between Incident Response and other nodes
MATCH (incident:Keyword {name: 'Incident Response'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (incident)-[:ALIGN_WITH]->(ethics);

MATCH (incident:Keyword {name: 'Incident Response'}), (transparency:Keyword {name: 'Transparency'})
CREATE (incident)-[:REQUIRES]->(transparency);

MATCH (incident:Keyword {name: 'Incident Response'}), (account:Keyword {name: 'Accountability'})
CREATE (incident)-[:ESTABLISHES]->(account);

MATCH (incident:Keyword {name: 'Incident Response'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (incident)-[:SUPPORTS]->(bias);

MATCH (incident:Keyword {name: 'Incident Response'}), (fairness:Keyword {name: 'Fairness'})
CREATE (incident)-[:ENSURES]->(fairness);

MATCH (incident:Keyword {name: 'Incident Response'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (incident)-[:PROTECTS]->(privacy);

MATCH (incident:Keyword {name: 'Incident Response'}), (protection:Keyword {name: 'Data Protection'})
CREATE (incident)-[:REINFORCES]->(protection);

MATCH (incident:Keyword {name: 'Incident Response'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (incident)-[:ENSURES]->(regulatory);

MATCH (incident:Keyword {name: 'Incident Response'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (incident)-[:MANDATES]->(gdpr);

MATCH (incident:Keyword {name: 'Incident Response'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (incident)-[:REQUIRES]->(audit);

MATCH (incident:Keyword {name: 'Incident Response'}), (explain:Keyword {name: 'Explainability'})
CREATE (incident)-[:PROVIDES]->(explain);

MATCH (incident:Keyword {name: 'Incident Response'}), (robust:Keyword {name: 'Robustness'})
CREATE (incident)-[:ENSURES]->(robust);

MATCH (incident:Keyword {name: 'Incident Response'}), (security:Keyword {name: 'Security'})
CREATE (incident)-[:MAINTAINS]->(security);

MATCH (incident:Keyword {name: 'Incident Response'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (incident)-[:REQUIRES]->(oversight);

MATCH (incident:Keyword {name: 'Incident Response'}), (governance:Keyword {name: 'Data Governance'})
CREATE (incident)-[:ALIGN_WITH]->(governance);

MATCH (incident:Keyword {name: 'Incident Response'}), (risk:Keyword {name: 'Risk Management'})
CREATE (incident)-[:INTEGRAL_TO]->(risk);

MATCH (incident:Keyword {name: 'Incident Response'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (incident)-[:SUPPORTS]->(ethical);

MATCH (incident:Keyword {name: 'Incident Response'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (incident)-[:ENSURES]->(accountability);

MATCH (incident:Keyword {name: 'Incident Response'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (incident)-[:RELIES_ON]->(monitoring);

MATCH (incident:Keyword {name: 'Incident Response'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (incident)-[:SUPPORTED_BY]->(compliance);

MATCH (incident:Keyword {name: 'Incident Response'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (incident)-[:INVOLVES]->(engagement);

MATCH (incident:Keyword {name: 'Incident Response'}), (responsible:Keyword {name: 'Responsible AI'})
CREATE (incident)-[:INTEGRAL_TO]->(responsible);

MATCH (incident:Keyword {name: 'Incident Response'}), (trust:Keyword {name: 'Trustworthiness'})
CREATE (incident)-[:BUILDS]->(trust);

MATCH (incident:Keyword {name: 'Incident Response'}), (consent:Keyword {name: 'Informed Consent'})
CREATE (incident)-[:RESPECTS]->(consent);

MATCH (incident:Keyword {name: 'Incident Response'}), (impact:Keyword {name: 'Impact Assessment'})
CREATE (incident)-[:RELIES_ON]->(impact);

MATCH (incident:Keyword {name: 'Incident Response'}), (diversity:Keyword {name: 'Diversity in AI'})
CREATE (incident)-[:CONSIDERS]->(diversity);

MATCH (incident:Keyword {name: 'Incident Response'}), (vendor:Keyword {name: 'Vendor Compliance'})
CREATE (incident)-[:REQUIRES]->(vendor);

MATCH (incident:Keyword {name: 'Incident Response'}), (policy:Keyword {name: 'Usage Policies'})
CREATE (incident)-[:GUIDED_BY]->(policy);
