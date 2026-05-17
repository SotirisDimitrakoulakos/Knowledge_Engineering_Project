//create constraints to ensure uniqueness
CREATE CONSTRAINT IF NOT EXISTS FOR (c:Country) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Month) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE;

//create the core structural nodes
MERGE (:Country {id: 'NL'})
MERGE (:Country {id: 'DE'})
MERGE (:Country {id: 'FR'})
MERGE (:Country {id: 'UK'});

MERGE (:Topic {name: 'Inflation'})
MERGE (:Topic {name: 'Housing'})
MERGE (:Topic {name: 'Employment'});


LOAD CSV WITH HEADERS FROM 'file:///eurostat_inflation.csv' AS row
//month node exists
MERGE (m:Month {id: row.Month})
//match the Country node
MATCH (c:Country {id: row.Country})
MATCH (t:Topic {name: 'Inflation'})
//create the Economic Indicator Node connecting Country and Month
CREATE (e:EconomicIndicator {
    value: toFloat(row.Inflation_Rate),
    type: 'HICP'
})
//create the Edges
CREATE (e)-[:REPORTED_FOR]->(m)
CREATE (e)-[:REPORTED_IN]->(c)
CREATE (e)-[:MEASURES]->(t);

LOAD CSV WITH HEADERS FROM 'file:///gdelt_curated_monthly.csv' AS row
MERGE (m:Month {id: row.Month})
MATCH (c:Country {id: row.Country})
MATCH (t:Topic {name: row.Topic})
//create the Media Narrative Node
CREATE (n:MediaNarrative {
    sentiment: toFloat(row.AverageSentiment),
    volume: toInteger(row.ArticleVolume)
})

//create the Edges
CREATE (n)-[:PUBLISHED_IN_MONTH]->(m)
CREATE (n)-[:PUBLISHED_IN_COUNTRY]->(c)
CREATE (n)-[:DISCUSSES]->(t);
