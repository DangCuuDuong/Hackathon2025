import pandas as pd
df = pd.read_csv("train_features.csv")
print(df['label'].value_counts())
