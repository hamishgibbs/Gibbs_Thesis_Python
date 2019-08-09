#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 09:50:40 2019

@author: hamishgibbs
"""

#import urllib
#import urllib.parse as urlp
import requests
import json
#import xml.etree.ElementTree as ET
import xmljson
from lxml.etree import fromstring
import zipfile
import io
import pandas as pd
#%%
url = "https://scihub.copernicus.eu/dhus/search?start=0&rows=100&q="
sensor = 'platformname:"Sentinel-2"'
footprint = 'footprint:"intersects(3.502020,-76.355062)"'
ccp= 'cloudcoverpercentage:[0 TO 30]'
date = 'ingestiondate:[2016-01-01T00:00:00.000Z TO NOW]'
#%%
rurl = url + sensor + ' AND ' + footprint + ' AND ' + ccp + ' AND ' + date
print(rurl)
#%%
r = requests.get(rurl, auth=('hamishgibbs', 'Hamish123!'))
#%%
xml = bytes(bytearray(r.text, encoding = 'utf-8'))
xml = fromstring(xml)
json1 = json.dumps(xmljson.badgerfish.data(xml))
#%%
data = json.loads(json1)
#%%
records = data['{http://www.w3.org/2005/Atom}feed']['{http://a9.com/-/spec/opensearch/1.1/}totalResults']['$']
print('Number of Scenes: ' + str(records))
if records > 100:
  print('WARNING: More than 100 results, adjust paging options.')
 #%%
#These are the ids, loop through all entrys and store in a list
ids = [None] * records
titles = [None] * records
dates = [None] * records
for i in range(0,(records)):
  ids[i] = data['{http://www.w3.org/2005/Atom}feed']['{http://www.w3.org/2005/Atom}entry'][i]['{http://www.w3.org/2005/Atom}id']['$']
  titles[i] = data['{http://www.w3.org/2005/Atom}feed']['{http://www.w3.org/2005/Atom}entry'][i]['{http://www.w3.org/2005/Atom}title']['$']
  dates[i] = data['{http://www.w3.org/2005/Atom}feed']['{http://www.w3.org/2005/Atom}entry'][i]['{http://www.w3.org/2005/Atom}date'][1]['$'][0:10]
ids
titles
dates
#%%
#Save Quicklook jpgs
ql = [None] * (records - 1)

for i in range(0,(records-1)):
  ql[i] = data['{http://www.w3.org/2005/Atom}feed']['{http://www.w3.org/2005/Atom}entry'][i]['{http://www.w3.org/2005/Atom}link'][2]['@href']
#%%
path = '/Volumes/Gibbs_Drive/S2 Quicklooks/'
for i, url in enumerate(ql):
  file_name = path + titles[i] + '.jpg'
  print(url)
  print(file_name)
  r = requests.get(url, auth=('hamishgibbs', 'Hamish123!'), stream=True)
  if r.status_code == 200:
    with open(file_name, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192): 
                if chunk: 
                    f.write(chunk)

#%%
print(len(ids), len(dates))
csv_data = {'ID': ids, 'DATE': dates, 'TITLE': titles}
csv_data = pd.DataFrame(csv_data)
csv_data.to_csv('/Volumes/Gibbs_Drive/Sentinel_Test/Sen2_Dates.csv', sep=',')
#%%
#Data Download
durl = 'https://scihub.copernicus.eu/apihub/odata/v1/Products('
id = "'4eac2f2c-faed-4557-8883-849224120760'"
other = ')' + '/$value'
dwurl = durl + id + other
dwurl
#%%
r = requests.get(dwurl, auth=('hamishgibbs', 'Hamish123!'))
#%%
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall('/Volumes/Seagate Expansion Drive/Sentinel_Test')
#%%
for i, value in enumerate(ids):
    id = "'" + value + "'"
    dwurl = durl + id + other
    r = requests.get(dwurl, auth=('hamishgibbs', 'Hamish123!'))
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall('/Volumes/Seagate Expansion Drive/Sentinel 2 Data')
    print('Scene ' + str((i + 1)) + ' of ' + str(records) + 'downloaded')


