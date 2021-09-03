# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 09:39:05 2021

@author: Leonard
"""

import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import os
storage_quality = pd.read_csv('Storage_exposed.csv')
storage_quality.head()
storage_quality["DateTime"] = pd.to_datetime(storage_quality["DateTime"])
time = storage_quality["DateTime"]
Timedelta = time.max()- time.min()
storage_quality["month"] = storage_quality["DateTime"].dt.month
fig, axs = plt.subplots(figsize=(12, 4))
axs.xaxis.set_ticklabels([])
data_in_month = storage_quality.groupby(storage_quality["DateTime"].dt.weekday)["Storage3"].plot(kind='bar', rot=0, ax=axs)
storage_quality.index = storage_quality["DateTime"]
# d1 = pd.to_datetime('2021-06-23')
# d2 = d1+pd.to_timedelta(30,unit='D')
start_day = '23'
start_month= 'June'
start_year= '2021'

end_day = '07'
end_month= 'July'
end_year= '2021'
#'24th of April, 2020'
time1_df = start_day+'th'+' of'+' '+start_month+', '+start_year
time2_df = end_day+'th'+' of'+' '+end_month+', '+end_year
d1 = pd.to_datetime(time1_df)
d2 = pd.to_datetime(time2_df)
tt = storage_quality[d1:d2]
str3 =sum( tt["Storage3"])
fig, axs = plt.subplots(figsize=(12, 4))
axs.xaxis.set_ticklabels([])
tt["Storage3"].plot(style="-o", figsize=(10, 5));
tt["Storage1"].plot(style="-o", figsize=(10, 5));
tt["Storage2"].plot(style="-o", figsize=(10, 5));

total = sum(storage_quality["Storage3"])