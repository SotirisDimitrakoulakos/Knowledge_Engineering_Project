import pandas as pd
import eurostat

# 1. Fetch Eurostat Data
print("Fetching Eurostat Inflation Data...")
# prc_hicp_midx is the Eurostat code for Harmonised index of consumer prices
df_inflation = eurostat.get_data_df('prc_hicp_midx')

# Filter for our countries and the general index (CP00)
countries = ['NL', 'DE', 'FR', 'UK']
df_inf_filtered = df_inflation[(df_inflation['geo\\TIME_PERIOD'].isin(countries)) & (df_inflation['coicop'] == 'CP00')]

# Melt the dataframe to get a clean Month-Year format
df_inf_clean = df_inf_filtered.melt(id_vars=['geo\\TIME_PERIOD', 'coicop'], 
                                    value_vars=[col for col in df_inf_filtered.columns if '202' in col],
                                    var_name='Month', value_name='Inflation_Rate')
df_inf_clean.rename(columns={'geo\\TIME_PERIOD': 'Country'}, inplace=True)

# Save to CSV for Neo4j
df_inf_clean.to_csv('eurostat_inflation.csv', index=False)
print("Eurostat data saved.")

import numpy as np

print("Curating GDELT Data...")
# Load the BigQuery CSV
df_gdelt = pd.read_csv('gdelt_raw.csv')

# The V2Tone column is a comma-separated string. The first number is the overall sentiment.
df_gdelt['SentimentScore'] = df_gdelt['tone'].apply(lambda x: float(str(x).split(',')[0]) if pd.notnull(x) else 0)

# Create a Year-Month column to link with Eurostat data (e.g., '2023-05')
df_gdelt['Month'] = df_gdelt['publish_date'].str[:7]

# Extract the primary country and topic for simplicity in this prototype
df_gdelt['Country'] = np.where(df_gdelt['locations'].str.contains('NL'), 'NL',
                      np.where(df_gdelt['locations'].str.contains('GM'), 'DE', # GDELT uses GM for Germany
                      np.where(df_gdelt['locations'].str.contains('FR'), 'FR', 'UK')))

df_gdelt['Topic'] = np.where(df_gdelt['themes'].str.contains('INFLATION'), 'Inflation',
                    np.where(df_gdelt['themes'].str.contains('HOUSING'), 'Housing', 'Employment'))

# We don't need every single article, we need the monthly aggregate for the graph
gdelt_monthly = df_gdelt.groupby(['Month', 'Country', 'Topic'])['SentimentScore'].agg(['mean', 'count']).reset_index()
gdelt_monthly.rename(columns={'mean': 'AverageSentiment', 'count': 'ArticleVolume'}, inplace=True)

gdelt_monthly.to_csv('gdelt_curated_monthly.csv', index=False)
print("GDELT Curated data saved.")