import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




df = pd.read_csv(r"C:\Users\ALEX\HardHack\plants.csv")
df = df[df["Fertilization Type"].isin(['Organic', "Balanced"])]
df = df[df['Soil'].isin(["well-drained"])]
df = df.get(['Plant Name', 'Sunlight', 'Watering'])
df = df.reset_index().drop('index', axis=1)
df['Watering'] = df['Watering'].apply(lambda x: x.lower())


def regularize_watering(x):
    categories = ['dry', 'moist', 'regular']
    if x == "regular, well-drained soil":
        return categories[2]
    elif x == "regular, moist soil":
        return categories[1]
    elif x == "water weekly":
        return categories[2]
    elif x == "regular watering":
        return categories[2]
    elif 'dry' in x.split():
        return categories[0]
    elif 'moist' in x.split():
        return categories[1]
    else:
        return categories[2]

def regularize_sun(x):
    x =  x.split()[0]
    if x == 'full':
        return 1
    elif x == 'partial':
        return 0.5
    else:
        return 0

print(df['Sunlight'].value_counts())

df['Watering'] = df['Watering'].apply(regularize_watering)
df["Sunlight"] = df["Sunlight"].apply(regularize_sun)
print(df)
df.iloc[:10].to_csv("small_cleaned_plants.csv", index=False)

print(df.set_index(['Sunlight', 'Watering']))
print(df.to_xarray())