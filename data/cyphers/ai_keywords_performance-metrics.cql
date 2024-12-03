// Create the Performance Metrics node
CREATE (:Keyword {name: 'Performance Metrics'});

// Add relationships between Performance Metrics and other nodes
MATCH (metrics:Keyword {name: 'Performance Metrics'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (metrics)-[:EVALUATES]->(ethics);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (transparency:Keyword {name: 'Transparency'})
CREATE (metrics)-[:SUPPORTS]->(transparency);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (account:Keyword {name: 'Accountability'})
CREATE (metrics)-[:MEASURES]->(account);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (metrics)-[:ASSESS]->(bias);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (fairness:Keyword {name: 'Fairness'})
CREATE (metrics)-[:ENSURES]->(fairness);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (metrics)-[:VALIDATES]->(privacy);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (protection:Keyword {name: 'Data Protection'})
CREATE (metrics)-[:EVALUATES]->(protection);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (metrics)-[:MEASURES]->(regulatory);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (metrics)-[:ALIGNS_WITH]->(gdpr);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (metrics)-[:SUPPORTS]->(audit);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (explain:Keyword {name: 'Explainability'})
CREATE (metrics)-[:MEASURES]->(explain);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (robust:Keyword {name: 'Robustness'})
CREATE (metrics)-[:ENSURES]->(robust);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (security:Keyword {name: 'Security'})
CREATE (metrics)-[:VALIDATES]->(security);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (metrics)-[:SUPPORTS]->(oversight);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (governance:Keyword {name: 'Data Governance'})
CREATE (metrics)-[:ENHANCES]->(governance);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (risk:Keyword {name: 'Risk Management'})
CREATE (metrics)-[:SUPPORTS]->(risk);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (metrics)-[:MEASURES]->(ethical);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (metrics)-[:EVALUATES]->(accountability);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (metrics)-[:SUPPORTS]->(monitoring);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (metrics)-[:INFORMS]->(compliance);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (metrics)-[:EVALUATES]->(engagement);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (responsible:Keyword {name: 'Responsible AI'})
CREATE (metrics)-[:SUPPORTS]->(responsible);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (trust:Keyword {name: 'Trustworthiness'})
CREATE (metrics)-[:BUILDS]->(trust);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (consent:Keyword {name: 'Informed Consent'})
CREATE (metrics)-[:SUPPORTS]->(consent);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (impact:Keyword {name: 'Impact Assessment'})
CREATE (metrics)-[:MEASURES]->(impact);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (diversity:Keyword {name: 'Diversity in AI'})
CREATE (metrics)-[:SUPPORTS]->(diversity);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (vendor:Keyword {name: 'Vendor Compliance'})
CREATE (metrics)-[:EVALUATES]->(vendor);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (policy:Keyword {name: 'Usage Policies'})
CREATE (metrics)-[:SUPPORTS]->(policy);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (incident:Keyword {name: 'Incident Response'})
CREATE (metrics)-[:EVALUATES]->(incident);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (landscape:Keyword {name: 'Regulatory Landscape'})
CREATE (metrics)-[:ALIGNS_WITH]->(landscape);

MATCH (metrics:Keyword {name: 'Performance Metrics'}), (benchmark:Keyword {name: 'Benchmarking'})
CREATE (metrics)-[:SUPPORTED_BY]->(benchmark);
