MATCH (c:Country)<-[:PUBLISHED_IN_COUNTRY]-(mn:MediaNarrative)-[:DISCUSSES]->(t:Topic)
MATCH (mn)-[:PUBLISHED_IN_MONTH]->(m:Month)
WITH c.id AS Country, t.id AS Topic, m.id AS Month, 
     sum(mn.article_volume) AS MonthlyVolume, 
     avg(mn.sentiment) AS MonthlySentiment
ORDER BY Country, Topic, Month
RETURN Country, Topic, Month, MonthlyVolume, MonthlySentiment