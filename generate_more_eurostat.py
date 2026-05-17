import pandas as pd
import eurostat

# Define our target countries (Eurostat uses 'UK' for the United Kingdom)
target_countries = ['NL', 'DE', 'FR', 'UK']

def generate_employment_csv():
    print("Fetching Unemployment data from Eurostat (une_rt_m)...")
    df = eurostat.get_data_df('une_rt_m')
    
    # Locate the exact name of the geo column
    geo_col = [c for c in df.columns if 'geo' in c.lower()][0]
    
    # Filter for the "Total" population (preventing duplicate rows for different age/gender brackets)
    if 'age' in df.columns:
        df = df[df['age'] == 'TOTAL']
    if 'sex' in df.columns:
        df = df[df['sex'] == 'T']
    if 'unit' in df.columns:
        df = df[df['unit'] == 'PC_ACT'] # Percentage of active population
        
    df = df[df[geo_col].isin(target_countries)]
    
    # Smart time column finder: Grab any column that starts with '20' (e.g., '2023-05', '2023M05')
    time_cols = [c for c in df.columns if str(c).startswith('20')]
    df = df[[geo_col] + time_cols]
    
    # Melt from wide to long
    df_melted = df.melt(id_vars=[geo_col], var_name='Month_Raw', value_name='Unemployment_Rate')
    df_melted = df_melted.dropna(subset=['Unemployment_Rate'])
    df_melted.rename(columns={geo_col: 'Country'}, inplace=True)
    
    # Normalize month format to standard 'YYYY-MM'
    df_melted['Month'] = df_melted['Month_Raw'].astype(str).str.replace('M', '-')
    
    # Filter for our 2020-2025 window
    df_final = df_melted[(df_melted['Month'] >= '2020-01') & (df_melted['Month'] <= '2025-12')]
    
    # Group by just in case, ensuring clean data
    df_final = df_final.groupby(['Month', 'Country'])['Unemployment_Rate'].mean().reset_index()
    
    df_final.to_csv('eurostat_employment.csv', index=False)
    print(f"Success! Saved eurostat_employment.csv with {len(df_final)} rows.")


def generate_housing_csv():
    print("Fetching Housing data from Eurostat (prc_hpi_q)...")
    df = eurostat.get_data_df('prc_hpi_q')
    
    geo_col = [c for c in df.columns if 'geo' in c.lower()][0]
    
    # Fix 1: Eurostat's actual code for 2015=100 is 'I15'
    if 'unit' in df.columns:
        if 'I15' in df['unit'].values:
            df = df[df['unit'] == 'I15']
            
    # Fix 2: Ensure we are grabbing the 'TOTAL' housing market (not split by new/existing)
    if 'purchase' in df.columns:
        df = df[df['purchase'] == 'TOTAL']
        
    df = df[df[geo_col].isin(target_countries)]
    
    time_cols = [c for c in df.columns if str(c).startswith('20')]
    df = df[[geo_col] + time_cols]
    
    df_melted = df.melt(id_vars=[geo_col], var_name='Quarter_Raw', value_name='House_Price_Index')
    df_melted = df_melted.dropna(subset=['House_Price_Index'])
    df_melted.rename(columns={geo_col: 'Country'}, inplace=True)
    
    def quarter_to_month(q_str):
        q_str = str(q_str).replace('-', '') # Standardize string to '2023Q1'
        year = q_str[:4]
        quarter = q_str[-2:]
        quarter_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
        return f"{year}-{quarter_map.get(quarter, '01')}"
        
    df_melted['Month'] = df_melted['Quarter_Raw'].apply(quarter_to_month)
    
    # Filter for our 2020-2025 window
    df_final = df_melted[(df_melted['Month'] >= '2020-01') & (df_melted['Month'] <= '2025-12')]
    
    df_final = df_final.groupby(['Month', 'Country'])['House_Price_Index'].mean().reset_index()
    
    df_final.to_csv('eurostat_housing.csv', index=False)
    print(f"Success! Saved eurostat_housing.csv with {len(df_final)} rows.")

# Execute the script
if __name__ == "__main__":
    generate_employment_csv()
    generate_housing_csv()