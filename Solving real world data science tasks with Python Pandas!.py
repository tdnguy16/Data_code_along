import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt


### Merge 12 months data in to a single file
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

data_lists = []

for month in months:
    month = pd.read_csv(f'Sales_{month}_2019.csv')
    data_lists.append(month)

data = pd.concat(data_lists)
data.set_index("Order ID", inplace = True)

# CLEAN HEADERS FROM DIFFERENT CSV FILES
data_clean = data.drop(index="Order ID")

print(data_clean.columns)

# HANDLE MISSING DATA
data_clean.fillna(0)

# CHANGE TYPE OF DATA COLUMNS
data_clean['Quantity Ordered'] = pd.to_numeric(data_clean['Quantity Ordered'])
data_clean['Price Each'] = pd.to_numeric(data_clean['Price Each'])

# CREATE A MONTH COLUMN
month_list = []
for date in data_clean['Order Date']:
    if type(date) == str:
        x = date[0:2]
        month_list.append(x)
    else:
        month_list.append(date)

data_clean['Month'] = month_list

# CREATE A SALE = QUANTITY * PRICE COLUMN
data_clean['Sale'] = data_clean['Quantity Ordered'] * data_clean['Price Each']

# SALE OF EACH MONTH
monthly_sale = data_clean.groupby('Month').sum()

with pd.option_context('display.max_columns', None):  # more options can be specified also
    print(data_clean)

# PLOT MONTHLY SALES
plt.bar(months, monthly_sale['Sale'])
plt.xticks(months)
plt.ylabel('Sales in USD')
plt.xlabel('Month number')
plt.show()




