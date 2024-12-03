// Create the Cultural Sensitivity node
CREATE (:Keyword {name: 'Cultural Sensitivity'});

// Add relationships between Cultural Sensitivity and other nodes
MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (sensitivity)-[:ENHANCES]->(ethics);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (transparency:Keyword {name: 'Transparency'})
CREATE (sensitivity)-[:SUPPORTS]->(transparency);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (account:Keyword {name: 'Accountability'})
CREATE (sensitivity)-[:ENSURES]->(account);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (sensitivity)-[:MITIGATES]->(bias);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (fairness:Keyword {name: 'Fairness'})
CREATE (sensitivity)-[:PROMOTES]->(fairness);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (sensitivity)-[:ALIGNS_WITH]->(privacy);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (protection:Keyword {name: 'Data Protection'})
CREATE (sensitivity)-[:INFORMS]->(protection);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (sensitivity)-[:SUPPORTS]->(regulatory);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (sensitivity)-[:ALIGN_WITH]->(gdpr);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (sensitivity)-[:INFORMS]->(audit);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (explain:Keyword {name: 'Explainability'})
CREATE (sensitivity)-[:ENHANCES]->(explain);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (robust:Keyword {name: 'Robustness'})
CREATE (sensitivity)-[:SUPPORTS]->(robust);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (security:Keyword {name: 'Security'})
CREATE (sensitivity)-[:INFORMS]->(security);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (sensitivity)-[:SUPPORTS]->(oversight);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (governance:Keyword {name: 'Data Governance'})
CREATE (sensitivity)-[:INFORMS]->(governance);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (risk:Keyword {name: 'Risk Management'})
CREATE (sensitivity)-[:SUPPORTS]->(risk);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (sensitivity)-[:INTEGRATES]->(ethical);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (sensitivity)-[:SUPPORTS]->(accountability);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (sensitivity)-[:INFORMS]->(monitoring);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (sensitivity)-[:ENHANCES]->(compliance);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (sensitivity)-[:PROMOTES]->(engagement);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (responsible:Keyword {name: 'Responsible AI'})
CREATE (sensitivity)-[:SUPPORTS]->(responsible);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (trust:Keyword {name: 'Trustworthiness'})
CREATE (sensitivity)-[:BUILDS]->(trust);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (consent:Keyword {name: 'Informed Consent'})
CREATE (sensitivity)-[:INFORMS]->(consent);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (impact:Keyword {name: 'Impact Assessment'})
CREATE (sensitivity)-[:INFORMS]->(impact);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (diversity:Keyword {name: 'Diversity in AI'})
CREATE (sensitivity)-[:SUPPORTS]->(diversity);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (vendor:Keyword {name: 'Vendor Compliance'})
CREATE (sensitivity)-[:REQUIRES]->(vendor);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (policy:Keyword {name: 'Usage Policies'})
CREATE (sensitivity)-[:INFORMS]->(policy);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (incident:Keyword {name: 'Incident Response'})
CREATE (sensitivity)-[:SUPPORTS]->(incident);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (landscape:Keyword {name: 'Regulatory Landscape'})
CREATE (sensitivity)-[:INTEGRATES]->(landscape);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (benchmark:Keyword {name: 'Benchmarking'})
CREATE (sensitivity)-[:INFORMS]->(benchmark);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (metrics:Keyword {name: 'Performance Metrics'})
CREATE (sensitivity)-[:SUPPORTS]->(metrics);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (adaptive:Keyword {name: 'Adaptive Compliance'})
CREATE (sensitivity)-[:SUPPORTS]->(adaptive);

MATCH (sensitivity:Keyword {name: 'Cultural Sensitivity'}), (minimization:Keyword {name: 'Data Minimization'})
CREATE (sensitivity)-[:ALIGNS_WITH]->(minimization);
