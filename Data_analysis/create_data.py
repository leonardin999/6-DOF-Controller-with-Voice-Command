# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 08:51:01 2021

@author: Leonard
"""

from datetime import time,date,datetime
import calendar
import numpy as np
import random
import pandas as pd

Date = pd.date_range(start = '2021/3/2',end = '2021/8/5',freq = 'D')
print(Date)

storage1_data = []
storage2_data = []
storage3_data = []
parameter_data =[]
Country_data =[]
for i in range(len(Date)):
    storage1_data.append(random.randint(80,150))
    storage2_data.append(random.randint(60,100))
    storage3_data.append(random.randint(30,200))
    parameter_data.append('Products')
    Country_data.append('VN')
df = pd.DataFrame()
df['DateTime'] = Date
# df['Country'] = Country_data
# df['Day'] = df['DateTime'].dt.day
# df['Month'] = df['DateTime'].dt.day
# df['Year'] = df['DateTime'].dt.day
df['Storage1'] = storage1_data
df['Storage2'] = storage2_data
df['Storage3'] = storage3_data
# df['Parameters'] = parameter_data
df.head()
# writer = pd.ExcelWriter("Data_store.xlsx",
#                         date_format='mmmm dd yyyy')

# # Convert the dataframe to an XlsxWriter Excel object.
df.to_csv(r'Storage_exposed.csv', index = False, header=True)