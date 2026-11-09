import pandas as pd
df = pd.read_csv('data/raw/cardekho_dataset.csv')
brands = sorted(df['brand'].unique())
print('Unique:', len(brands))
for b in brands:
    print(repr(b))
