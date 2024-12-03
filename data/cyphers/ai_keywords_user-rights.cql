// Create the User Rights node
CREATE (:Keyword {name: 'User Rights'});

// Add relationships between User Rights and other nodes
MATCH (rights:Keyword {name: 'User Rights'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (rights)-[:SUPPORTS]->(ethics);

MATCH (rights:Keyword {name: 'User Rights'}), (transparency:Keyword {name: 'Transparency'})
CREATE (rights)-[:REQUIRES]->(transparency);

MATCH (rights:Keyword {name: 'User Rights'}), (account:Keyword {name: 'Accountability'})
CREATE (rights)-[:ENSURES]->(account);

MATCH (rights:Keyword {name: 'User Rights'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (rights)-[:PROMOTES]->(bias);

MATCH (rights:Keyword {name: 'User Rights'}), (fairness:Keyword {name: 'Fairness'})
CREATE (rights)-[:SUPPORTS]->(fairness);

MATCH (rights:Keyword {name: 'User Rights'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (rights)-[:PROTECTS]->(privacy);

MATCH (rights:Keyword {name: 'User Rights'}), (protection:Keyword {name: 'Data Protection'})
CREATE (rights)-[:REQUIRES]->(protection);

MATCH (rights:Keyword {name: 'User Rights'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (rights)-[:ENFORCED_BY]->(regulatory);

MATCH (rights:Keyword {name: 'User Rights'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (rights)-[:ENSURED_BY]->(gdpr);

MATCH (rights:Keyword {name: 'User Rights'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (rights)-[:REQUIRES]->(audit);

MATCH (rights:Keyword {name: 'User Rights'}), (explain:Keyword {name: 'Explainability'})
CREATE (rights)-[:REQUIRES]->(explain);

MATCH (rights:Keyword {name: 'User Rights'}), (robust:Keyword {name: 'Robustness'})
CREATE (rights)-[:ENSURES]->(robust);

MATCH (rights:Keyword {name: 'User Rights'}), (security:Keyword {name: 'Security'})
CREATE (rights)-[:REQUIRES]->(security);

MATCH (rights:Keyword {name: 'User Rights'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (rights)-[:SUPPORTED_BY]->(oversight);

MATCH (rights:Keyword {name: 'User Rights'}), (governance:Keyword {name: 'Data Governance'})
CREATE (rights)-[:INTEGRATES_WITH]->(governance);

MATCH (rights:Keyword {name: 'User Rights'}), (risk:Keyword {name: 'Risk Management'})
CREATE (rights)-[:ADDRESSES]->(risk);

MATCH (rights:Keyword {name: 'User Rights'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (rights)-[:PROMOTES]->(ethical);

MATCH (rights:Keyword {name: 'User Rights'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (rights)-[:ENSURES]->(accountability);

MATCH (rights:Keyword {name: 'User Rights'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (rights)-[:SUPPORTS]->(monitoring);

MATCH (rights:Keyword {name: 'User Rights'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (rights)-[:INFORMS]->(compliance);

MATCH (rights:Keyword {name: 'User Rights'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (rights)-[:ENHANCES]->(engagement);

MATCH (rights:Keyword {name: 'User Rights'}), (responsible:Keyword {name: 'Responsible AI'})
CREATE (rights)-[:PROMOTES]->(responsible);

MATCH (rights:Keyword {name: 'User Rights'}), (trust:Keyword {name: 'Trustworthiness'})
CREATE (rights)-[:BUILDS]->(trust);

MATCH (rights:Keyword {name: 'User Rights'}), (consent:Keyword {name: 'Informed Consent'})
CREATE (rights)-[:REQUIRES]->(consent);

MATCH (rights:Keyword {name: 'User Rights'}), (impact:Keyword {name: 'Impact Assessment'})
CREATE (rights)-[:INTEGRATES_WITH]->(impact);

MATCH (rights:Keyword {name: 'User Rights'}), (diversity:Keyword {name: 'Diversity in AI'})
CREATE (rights)-[:PROMOTES]->(diversity);

MATCH (rights:Keyword {name: 'User Rights'}), (vendor:Keyword {name: 'Vendor Compliance'})
CREATE (rights)-[:ENFORCES]->(vendor);

MATCH (rights:Keyword {name: 'User Rights'}), (policy:Keyword {name: 'Usage Policies'})
CREATE (rights)-[:SHAPES]->(policy);

MATCH (rights:Keyword {name: 'User Rights'}), (incident:Keyword {name: 'Incident Response'})
CREATE (rights)-[:ENSURES]->(incident);

MATCH (rights:Keyword {name: 'User Rights'}), (landscape:Keyword {name: 'Regulatory Landscape'})
CREATE (rights)-[:INFORMS]->(landscape);

MATCH (rights:Keyword {name: 'User Rights'}), (benchmark:Keyword {name: 'Benchmarking'})
CREATE (rights)-[:INFORMS]->(benchmark);

MATCH (rights:Keyword {name: 'User Rights'}), (metrics:Keyword {name: 'Performance Metrics'})
CREATE (rights)-[:MEASURES]->(metrics);

MATCH (rights:Keyword {name: 'User Rights'}), (adaptive:Keyword {name: 'Adaptive Compliance'})
CREATE (rights)-[:INTEGRATES_WITH]->(adaptive);

MATCH (rights:Keyword {name: 'User Rights'}), (minimization:Keyword {name: 'Data Minimization'})
CREATE (rights)-[:SUPPORTS]->(minimization);

MATCH (rights:Keyword {name: 'User Rights'}), (sensitivity:Keyword {name: 'Cultural Sensitivity'})
CREATE (rights)-[:RESPECTS]->(sensitivity);
