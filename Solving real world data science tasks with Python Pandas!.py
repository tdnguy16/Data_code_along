import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from itertools import combinations
from collections import Counter
import matplotlib.pyplot as plt


### Merge 12 months data in to a single file
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

data_lists = []

for month in months:
    month = pd.read_csv(f'Sales_{month}_2019.csv')
    data_lists.append(month)

data = pd.concat(data_lists)

# CLEAN HEADERS FROM DIFFERENT CSV FILES
data_clean = data[data['Order ID'] != "Order ID"]

print(data_clean.columns)

# HANDLE MISSING DATA
data_clean.fillna('')

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


# PLOT MONTHLY SALES
# plt.bar(months, monthly_sale['Sale'])
# plt.xticks(months)
# plt.ylabel('Sales in USD')
# plt.xlabel('Month number')
# plt.show()

### WHAT CITY HAD THE HIGHEST NUMBER OF SALES
# SPLIT ADDRESS INTO SMALLER INFO
city_list = []
for address in data_clean['Purchase Address']:
    city = str(address).split(',')
    if len(city) < 3:
        city_list.append('')
    else:
        city_list.append(city[1])


# CREATE A CITY COLUMN
data_clean['City'] = city_list

# GET SALE BY CITY
city_sales = data_clean.groupby('City').sum()
# print(city_sales)

# PLOT City SALES
# cities = [city for city, Dataframe in data_clean.groupby('City')]
# plt.bar(cities, city_sales['Sale'])
# plt.xticks(cities, rotation='vertical', size=8)
# plt.ylabel('Sales in USD')
# plt.xlabel('City name')
# plt.show()

### BEST TIME FOR AD DISPLAY TO MAXIMIZE PRODUCT PURCHASE RATE
# CONVERT ORDER DATE COL TO A DATE_TIME PYTHON'S FORMAT
# data_clean['Order Date'] = pd.to_datetime(data_clean['Order Date'])
#
# data_clean['Hour'] = data_clean['Order Date'].dt.hour
# data_clean['Minute'] = data_clean['Order Date'].dt.minute
#
# hours = [hour for hour, df in data_clean.groupby('Hour')]
# plt.plot(hours, data_clean.groupby(['Hour']).count())
# plt.xticks(hours)
# plt.grid()
# plt.show()

### WHAT ITEMS ARE USUALLY SOLD TOGETHER
# Find all duplicated Order ID
multi_item_order = data_clean[data_clean.duplicated(['Order ID'], keep=False)]

# Group orders by Order ID
y = multi_item_order.groupby('Order ID')

# Combine products of the same order
z = y['Product'].apply(lambda x: ','.join(x))

# # Count unique pairs of products into a dict
count = Counter()
for sublist in z.values:
    sublist_list = sublist.split(',')
    count.update(Counter(combinations(sublist_list, 2)))
    count.update(Counter(combinations(sublist_list, 3)))
    count.update(Counter(combinations(sublist_list, 4)))
    count.update(Counter(combinations(sublist_list, 5)))
print(len(count))
print(count)

### PRINT THE WHOLE DATAFRAME
# with pd.option_context('display.max_columns', None):  # more options can be specified also
#     print(data_clean)
