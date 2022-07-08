import pandas as pd

df = pd.read_csv('logs.csv')
print(df)
print(type(df.iloc[:,3]))