#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 07:16:41 2019

@author: hamishgibbs
"""

import pandas as pd
#%%
S1 = pd.read_csv('/Volumes/Gibbs_Drive/Sentinel_Test/Sen1_Dates.csv', parse_dates = ['DATE'])
S2 = pd.read_csv('/Volumes/Gibbs_Drive/Sentinel_Test/Sen2_Dates.csv', parse_dates = ['DATE']) 
FW = pd.read_csv('/Volumes/Gibbs_Drive/Sentinel_Test/FW_Dates.csv', parse_dates = ['DATE'])
#%%
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))
#%%
csv_data = list()

for item in list(FW['DATE']):
    S1_Near = nearest(list(S1['DATE']), item)
    S1_Num = (S1_Near - item).days
    S2_Near = nearest(list(S2['DATE']), item)
    S2_Num = (S2_Near - item).days
    S2_Title = S2[S2['DATE'] == S2_Near].iloc[0,3]
    csv_data.append((item, S1_Near, S1_Num, S2_Near, S2_Num, S2_Title))
#%%
Nearest_DF = pd.DataFrame(csv_data)
Nearest_DF.columns = ['FW', 'S1', 'S1_Num', 'S2', 'S2_Num', 'S2_Title']
#%%
Nearest_DF.to_csv('/Volumes/Gibbs_Drive/Sentinel_Test/Nearest_Dates.csv')
#%%