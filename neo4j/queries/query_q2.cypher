MATCH (c:Country)<-[:PUBLISHED_IN_COUNTRY]-(mn:MediaNarrative)-[:DISCUSSES]->(t:Topic)
MATCH (mn)-[:PUBLISHED_IN_MONTH]->(m:Month)
// Pass the exact string identifiers through the barrier
WITH c.id AS Country, t.id AS Topic, m.id AS Month, percentileCont(mn.sentiment, 0.5) AS MedianSentiment

// Re-match the specific Country and Month nodes using those passed strings
MATCH (ei:EconomicIndicator)-[:REPORTED_FOR]->(:Month {id: Month})
MATCH (ei)-[:REPORTED_IN]->(:Country {id: Country})

// Use the 'Topic' string alias we passed through
WHERE ei.type CONTAINS Topic 

RETURN Country, Topic, Month, MedianSentiment, ei.value AS IndicatorValue
ORDER BY Country, Topic, Month