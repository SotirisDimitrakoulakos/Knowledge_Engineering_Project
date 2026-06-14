SELECT 
  CAST(DATE(PARSE_TIMESTAMP('%Y%m%d%H%M%S', CAST(DATE AS STRING))) AS STRING) as publish_date,
  DocumentIdentifier as url,
  V2Locations as locations,
  V2Themes as themes,
  V2Tone as tone,
  V2Organizations as organizations,
  V2Persons as persons
FROM 
  `gdelt-bq.gdeltv2.gkg_partitioned`
WHERE 
  _PARTITIONTIME >= TIMESTAMP('2021-01-01') 
  AND _PARTITIONTIME <= TIMESTAMP('2023-12-31')
  AND (V2Locations LIKE '%NL%' OR V2Locations LIKE '%GM%' OR V2Locations LIKE '%FR%' OR V2Locations LIKE '%UK%')
  AND (V2Themes LIKE '%ECON_INFLATION%' OR V2Themes LIKE '%ECON_HOUSING%' OR V2Themes LIKE '%UNEMPLOYMENT%')
