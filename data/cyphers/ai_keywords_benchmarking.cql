// Create the Benchmarking node
CREATE (:Keyword {name: 'Benchmarking'});

// Add relationships between Benchmarking and other nodes
MATCH (benchmark:Keyword {name: 'Benchmarking'}), (ethics:Keyword {name: 'AI Ethics'})
CREATE (benchmark)-[:PROMOTES]->(ethics);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (transparency:Keyword {name: 'Transparency'})
CREATE (benchmark)-[:IMPROVES]->(transparency);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (account:Keyword {name: 'Accountability'})
CREATE (benchmark)-[:SUPPORTS]->(account);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (bias:Keyword {name: 'Bias Mitigation'})
CREATE (benchmark)-[:EVALUATES]->(bias);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (fairness:Keyword {name: 'Fairness'})
CREATE (benchmark)-[:ENSURES]->(fairness);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (privacy:Keyword {name: 'Data Privacy'})
CREATE (benchmark)-[:ENHANCES]->(privacy);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (protection:Keyword {name: 'Data Protection'})
CREATE (benchmark)-[:MEASURES]->(protection);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (regulatory:Keyword {name: 'Regulatory Compliance'})
CREATE (benchmark)-[:ENSURES]->(regulatory);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (gdpr:Keyword {name: 'GDPR (General Data Protection Regulation)'})
CREATE (benchmark)-[:ALIGNS_WITH]->(gdpr);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (audit:Keyword {name: 'Audit Trails'})
CREATE (benchmark)-[:ASSESS]->(audit);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (explain:Keyword {name: 'Explainability'})
CREATE (benchmark)-[:IMPROVES]->(explain);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (robust:Keyword {name: 'Robustness'})
CREATE (benchmark)-[:ENSURES]->(robust);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (security:Keyword {name: 'Security'})
CREATE (benchmark)-[:EVALUATES]->(security);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (oversight:Keyword {name: 'Human Oversight'})
CREATE (benchmark)-[:SUPPORTS]->(oversight);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (governance:Keyword {name: 'Data Governance'})
CREATE (benchmark)-[:IMPROVES]->(governance);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (risk:Keyword {name: 'Risk Management'})
CREATE (benchmark)-[:SUPPORTS]->(risk);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (ethical:Keyword {name: 'Ethical AI'})
CREATE (benchmark)-[:EVALUATES]->(ethical);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (accountability:Keyword {name: 'Algorithmic Accountability'})
CREATE (benchmark)-[:SUPPORTS]->(accountability);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (monitoring:Keyword {name: 'Model Monitoring'})
CREATE (benchmark)-[:IMPROVES]->(monitoring);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (compliance:Keyword {name: 'Compliance Framework'})
CREATE (benchmark)-[:ALIGNS_WITH]->(compliance);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (engagement:Keyword {name: 'Stakeholder Engagement'})
CREATE (benchmark)-[:SUPPORTS]->(engagement);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (responsible:Keyword {name: 'Responsible AI'})
CREATE (benchmark)-[:EVALUATES]->(responsible);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (trust:Keyword {name: 'Trustworthiness'})
CREATE (benchmark)-[:BUILDS]->(trust);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (consent:Keyword {name: 'Informed Consent'})
CREATE (benchmark)-[:SUPPORTS]->(consent);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (impact:Keyword {name: 'Impact Assessment'})
CREATE (benchmark)-[:SUPPORTS]->(impact);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (diversity:Keyword {name: 'Diversity in AI'})
CREATE (benchmark)-[:HIGHLIGHTS]->(diversity);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (vendor:Keyword {name: 'Vendor Compliance'})
CREATE (benchmark)-[:ENSURES]->(vendor);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (policy:Keyword {name: 'Usage Policies'})
CREATE (benchmark)-[:EVALUATES]->(policy);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (incident:Keyword {name: 'Incident Response'})
CREATE (benchmark)-[:SUPPORTS]->(incident);

MATCH (benchmark:Keyword {name: 'Benchmarking'}), (landscape:Keyword {name: 'Regulatory Landscape'})
CREATE (benchmark)-[:ALIGNS_WITH]->(landscape);
