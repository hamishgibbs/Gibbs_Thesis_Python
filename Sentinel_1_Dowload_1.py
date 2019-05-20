#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:38:01 2019

@author: hamishgibbs
"""

import requests
import json
#import xml.etree.ElementTree as ET
import xmljson
from lxml.etree import fromstring
import zipfile
import io
from datetime import datetime
import pandas as pd
#%%
page = 0
url = 'https://scihub.copernicus.eu/dhus/search?start=' + str(page) + '&rows=100&q='
sensor = 'platformname:"Sentinel-1"'
footprint = 'footprint:"intersects(3.502020,-76.355062)"'
date = 'ingestiondate:[2016-01-01T00:00:00.000Z TO NOW]'
polarization = 'polarisationmode:VV VH'
mode = 'sensoroperationalmode:IW'
#%%
rurl = url + sensor + ' AND ' + footprint +  ' AND ' + date +  ' AND ' + polarization +  ' AND ' + mode
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
records
#%%
pages = [0,100,200,300,400]
data = []
for i, page in enumerate(pages):
    url = 'https://scihub.copernicus.eu/dhus/search?start=' + str(page) + '&rows=100&q='
    rurl = url + sensor + ' AND ' + footprint +  ' AND ' + date +  ' AND ' + polarization +  ' AND ' + mode
    r = requests.get(rurl, auth=('hamishgibbs', 'Hamish123!'))
    xml = bytes(bytearray(r.text, encoding = 'utf-8'))
    xml = fromstring(xml)
    json1 = json.dumps(xmljson.badgerfish.data(xml))
    data_temp = json.loads(json1)
    data = data + data_temp['{http://www.w3.org/2005/Atom}feed']['{http://www.w3.org/2005/Atom}entry'][0:100]
    print('Scene ' + str(page + 99) + ' of ' + str(records) + ' downloaded')
#%%
for record in data:
  if len(record) != 7:
    print('ERROR: Records do not match')
#%%
ids = list()
titles = [None] * records
for i, record in enumerate(data):
    ids.append(record['{http://www.w3.org/2005/Atom}id']['$'])
    titles[i] = record['{http://www.w3.org/2005/Atom}title']['$']
#%%
ids
titles
#%%
dates = list()
for i, record in enumerate(data):
  dates.append(record['{http://www.w3.org/2005/Atom}date'][1]['$'][0:10])
#%%
#print(len(ids), len(dates))
csv_data = {'ID': ids, 'DATE': dates, 'TITLE' : titles}
csv_data = pd.DataFrame(csv_data)
#%%
csv_data.to_csv('/Volumes/Gibbs_Drive/Sentinel_Test/Sen1_Dates.csv', sep=',')
#%%
date_convert = lambda x: datetime.strptime(x, '%Y-%m-%d')
date_list = list(map(date_convert, dates))

#Now: 
#find all Sen1 scenes on the same day as a multispectral acquisition


