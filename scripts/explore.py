import pandas as pd

df = pd.read_csv('data/raw/cardekho_dataset.csv')

print('--- Unnamed: 0 ---')
print(df['Unnamed: 0'].head())
print('range:', df['Unnamed: 0'].min(), '-', df['Unnamed: 0'].max())

print('\n--- brand (jumlah unik & 30 teratas) ---')
print('n unique:', df['brand'].nunique())
print(df['brand'].value_counts().head(30))

print('\n--- vehicle_age ---')
print(df['vehicle_age'].describe())
print('nilai unik:', sorted(df['vehicle_age'].unique()))

print('\n--- selling_price ---')
print(df['selling_price'].describe())
print('baris selling_price == 0:', (df['selling_price'] == 0).sum())
print('baris selling_price < 0  :', (df['selling_price'] < 0).sum())

print('\n--- fuel_type, seller_type, transmission_type ---')
for c in ['fuel_type', 'seller_type', 'transmission_type']:
    print(f'{c}:', df[c].value_counts().to_dict())

print('\n--- seats ---')
print(df['seats'].value_counts().sort_index())

print('\n--- mileage, engine, max_power ---')
print(df[['mileage', 'engine', 'max_power']].describe())
