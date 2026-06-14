/* Remove the UK media narratives */

MATCH (n:MediaNarrative)-[:PUBLISHED_IN_COUNTRY]->(:Country {id: 'UK'})
DETACH DELETE n

/* Remove the UK Economic Indicators */

MATCH (ei:EconomicIndicator)-[:REPORTED_IN]->(c:Country {id: 'UK'})
DETACH DELETE ei

/* Remove the UK Country Node */

MATCH (c:Country {id: 'UK'})
DELETE c