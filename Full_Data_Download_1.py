#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 20:48:35 2019

@author: hamishgibbs
"""

import pandas as pd
import requests
import zipfile
import io
#%%
#Get IDs for scenes that will be downloaded
S1 = pd.read_csv('/Volumes/Gibbs_Drive/Sentinel_Test/S1_Final_Scenes.csv', parse_dates=['DATE'])
S2 = pd.read_csv('/Volumes/Gibbs_Drive/Sentinel_Test/S2_Final_Scenes.csv', parse_dates=['DATE'])

print('Sentinel 1 Scenes: ')
print(S1['ID'])
print()
print('Sentinel 2 Scenes: ')
print(S2['ID'])
#%%
durl = 'https://scihub.copernicus.eu/apihub/odata/v1/Products('
other = ')' + '/$value'
#%%
dwurl = durl + str("'" + S2['ID'][0] + "'") + other
print(dwurl)
#%%
r = requests.get(dwurl, auth=('hamishgibbs', 'Hamish123!'))
print('requested')
#%%
z = zipfile.ZipFile(io.BytesIO(r.content))
print('zipped')
z.extractall('/Volumes/Gibbs_Drive/S2_Data_Palmira')
print('extracted')