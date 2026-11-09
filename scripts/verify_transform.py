import pandas as pd
df = pd.read_parquet('data/processed/transformed.parquet')
print('Shape:', df.shape)
print('Columns:', list(df.columns))
print('ISUZU masih ada?', 'ISUZU' in df['brand'].values)
print('Isuzu count:', (df['brand'] == 'Isuzu').sum())
print('seats=0 count:', (df['seats'] == 0).sum())
print('brand sample:', sorted(df['brand'].unique())[:5])
