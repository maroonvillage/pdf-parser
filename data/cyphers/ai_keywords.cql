CREATE (:Keyword {name: 'AI Ethics'}),
       (:Keyword {name: 'Transparency'}),
       (:Keyword {name: 'Accountability'}),
       (:Keyword {name: 'Bias Mitigation'}),
       (:Keyword {name: 'Fairness'}),
       (:Keyword {name: 'Data Privacy'}),
       (:Keyword {name: 'Data Protection'});


MATCH (a:Keyword {name: 'AI Ethics'}), (b:Keyword {name: 'Transparency'})
CREATE (a)-[:SUPPORTS]->(b);

MATCH (a:Keyword {name: 'AI Ethics'}), (b:Keyword {name: 'Accountability'})
CREATE (a)-[:ENSURES]->(b);

MATCH (a:Keyword {name: 'AI Ethics'}), (b:Keyword {name: 'Bias Mitigation'})
CREATE (a)-[:REQUIRES]->(b);

MATCH (a:Keyword {name: 'AI Ethics'}), (b:Keyword {name: 'Fairness'})
CREATE (a)-[:PROMOTES]->(b);


MATCH (a:Keyword {name: 'Transparency'}), (b:Keyword {name: 'Accountability'})
CREATE (a)-[:ENABLES]->(b);


MATCH (a:Keyword {name: 'Transparency'}), (b:Keyword {name: 'Data Privacy'})
CREATE (a)-[:INFORMS]->(b);

MATCH (a:Keyword {name: 'Accountability'}), (b:Keyword {name: 'Fairness'})
CREATE (a)-[:EVALUATES]->(b);


MATCH (a:Keyword {name: 'Accountability'}), (b:Keyword {name: 'Bias Mitigation'})
CREATE (a)-[:ASSESSES]->(b);


MATCH (a:Keyword {name: 'Bias Mitigation'}), (b:Keyword {name: 'Fairness'})
CREATE (a)-[:SUPPORTS]->(b);


MATCH (a:Keyword {name: 'Bias Mitigation'}), (b:Keyword {name: 'Data Privacy'})
CREATE (a)-[:REQUIRES]->(b);


MATCH (a:Keyword {name: 'Fairness'}), (b:Keyword {name: 'AI Ethics'})
CREATE (a)-[:ALIGNED_WITH]->(b);


MATCH (a:Keyword {name: 'Fairness'}), (b:Keyword {name: 'AI Ethics'})
CREATE (a)-[:REQUIRES]->(b);

MATCH (a:Keyword {name: 'Data Privacy'}), (b:Keyword {name: 'Data Protection'})
CREATE (a)-[:ALIGNED_WITH]->(b);

MATCH (a:Keyword {name: 'Data Privacy'}), (b:Keyword {name: 'AI Ethics'})
CREATE (a)-[:ALIGNED_WITH]->(b);


