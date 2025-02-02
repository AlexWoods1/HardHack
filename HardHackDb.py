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
#df.to_csv("small_cleaned_plants.csv", index=False)

print(df[(df['Sunlight'] == 1) & (df['Watering'] == 'moist')]['Plant Name'].to_list())
print(df[(df['Sunlight'] == 1) & (df['Watering'] == 'regular')]['Plant Name'].to_list())
print(df[(df['Sunlight'] == 1) & (df['Watering'] == 'dry')]['Plant Name'].to_list())

print(df[(df['Sunlight'] == 0.5) & (df['Watering'] == 'moist')]['Plant Name'].to_list())
print(df[(df['Sunlight'] == 0.5) & (df['Watering'] == 'regular')]['Plant Name'].to_list())
print(df[(df['Sunlight'] == 0.5) & (df['Watering'] == 'dry')]['Plant Name'].to_list())

print(df[(df['Sunlight'] == 0) & (df['Watering'] == 'moist')]['Plant Name'].to_list())
print(df[(df['Sunlight'] == 0) & (df['Watering'] == 'regular')]['Plant Name'].to_list())
print(df[(df['Sunlight'] == 0) & (df['Watering'] == 'dry')]['Plant Name'].to_list())


def User_number(x, y):
    if x == 1:
        if y == 'moist':
            return 1
        elif y == 'regular':
            return 2
        else:
            return 3
    elif x == 0.5:
        if y == 'moist':
            return 4
        elif y == 'regular':
            return 5
        else:
            return 6
    elif x == 0:
        if y == 'moist':
            return 7
        elif y == 'regular':
            return 8
        else:
            return 9


df = df.assign(control_num=df.get(["Sunlight", "Watering"]).apply(lambda row: User_number(row['Sunlight'], row['Watering']), axis=1))

df_simple = df.get(['Plant Name', 'control_num'])
df_simple = df_simple.assign(number=1)
df_simple = df_simple.groupby(['control_num', "Plant Name"]).nunique().reset_index().set_index('control_num').drop('number', axis=1)
df_simple.to_csv("Numeric_df.csv")
