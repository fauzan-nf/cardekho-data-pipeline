import pandas as pd
df = pd.read_parquet('data/processed/transformed.parquet')
for b in ['BMW', 'MG', 'Mercedes-AMG', 'Land Rover', 'Rolls-Royce', 'Bmw', 'Mg', 'Mercedes-Amg']:
    count = (df['brand'] == b).sum()
    if count > 0:
        print(f'{b}: {count}')
