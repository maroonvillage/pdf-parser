// Create the Data Minimization node
CREATE (:Keyword {name: 'Data Minimization'});

// Add relationships between Data Minimization and other nodes
MATCH (minimization:Keyword {name: 'Data Minimization'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (minimization)-[:SUPPORTS]->(ethics);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (transparency:Keyword {name: 'Transparency'})
CREATE (minimization)-[:ENHANCES]->(transparency);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (account:Keyword {name: 'Accountability'})
CREATE (minimization)-[:PROMOTES]->(account);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (minimization)-[:REDUCES]->(bias);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (fairness:Keyword {name: 'Fairness'})
CREATE (minimization)-[:ENSURES]->(fairness);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (minimization)-[:ALIGN_WITH]->(privacy);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (protection:Keyword {name: 'Data Protection'})
CREATE (minimization)-[:ENHANCES]->(protection);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (minimization)-[:SUPPORTS]->(regulatory);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (minimization)-[:MANDATED_BY]->(gdpr);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (minimization)-[:SIMPLIFIES]->(audit);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (explain:Keyword {name: 'Explainability'})
CREATE (minimization)-[:ENHANCES]->(explain);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (robust:Keyword {name: 'Robustness'})
CREATE (minimization)-[:SUPPORTS]->(robust);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (security:Keyword {name: 'Security'})
CREATE (minimization)-[:STRENGTHENS]->(security);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (minimization)-[:FOCUSES]->(oversight);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (governance:Keyword {name: 'Data Governance'})
CREATE (minimization)-[:INTEGRATES_WITH]->(governance);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (risk:Keyword {name: 'Risk Management'})
CREATE (minimization)-[:REDUCES]->(risk);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (minimization)-[:SUPPORTS]->(ethical);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (minimization)-[:ENHANCES]->(accountability);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (minimization)-[:FOCUSES]->(monitoring);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (minimization)-[:FOUNDATION_FOR]->(compliance);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (minimization)-[:SUPPORTS]->(engagement);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (responsible:Keyword {name: 'Responsible AI'})
CREATE (minimization)-[:ENSURES]->(responsible);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (trust:Keyword {name: 'Trustworthiness'})
CREATE (minimization)-[:BUILDS]->(trust);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (consent:Keyword {name: 'Informed Consent'})
CREATE (minimization)-[:SUPPORTS]->(consent);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (impact:Keyword {name: 'Impact Assessment'})
CREATE (minimization)-[:ENHANCES]->(impact);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (diversity:Keyword {name: 'Diversity in AI'})
CREATE (minimization)-[:SUPPORTS]->(diversity);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (vendor:Keyword {name: 'Vendor Compliance'})
CREATE (minimization)-[:REQUIRES]->(vendor);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (policy:Keyword {name: 'Usage Policies'})
CREATE (minimization)-[:INFORMS]->(policy);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (incident:Keyword {name: 'Incident Response'})
CREATE (minimization)-[:LIMITS]->(incident);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (landscape:Keyword {name: 'Regulatory Landscape'})
CREATE (minimization)-[:ALIGNS_WITH]->(landscape);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (benchmark:Keyword {name: 'Benchmarking'})
CREATE (minimization)-[:SETS]->(benchmark);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (metrics:Keyword {name: 'Performance Metrics'})
CREATE (minimization)-[:MEASURES]->(metrics);

MATCH (minimization:Keyword {name: 'Data Minimization'}), (adaptive:Keyword {name: 'Adaptive Compliance'})
CREATE (minimization)-[:SUPPORTS]->(adaptive);
