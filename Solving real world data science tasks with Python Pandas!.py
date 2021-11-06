import pandas as pd


# Merge 12 months data in to a single file
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

data_lists = []

for month in months:
    month = pd.read_csv(f'Sales_{month}_2019.csv')
    headers = month.iloc[0]
    data_lists.append(month)

data = pd.concat(data_lists)
data.set_index("Order ID", inplace = True)

print(data)

data_clean = data.drop(index="Order ID")
print(data_clean)

