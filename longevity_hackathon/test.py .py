

import pandas as pd

df = pd.read_csv('/Users/tarafriedrich/Downloads/skcm_polygon/TCGA-Z2-AA3S-01Z-00-DX1.EE957037-93E8-4BF2-A9E9-0F5A6760752D.svs.tar.gz/skcm_polygon/TCGA-Z2-AA3S-01Z-00-DX1.EE957037-93E8-4BF2-A9E9-0F5A6760752D.svs/100001*.csv')

print(df.head())

print(df.shape)

print(df.columns)