#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install pygrib


# In[ ]:


import pygrib


# In[ ]:


pip install cdsapi


# In[ ]:


import cdsapi
import numpy as np
import pandas as pd
from tqdm import tqdm
import time


# In[ ]:


# North, West, South, East
#ニューデリーは13：30。本当は0830指定だが、30分単位では指定できず

london = ["london",'14:00', 51.6, -0.3, 51.5, -0.2]
newyork = ['newyork', '19:00', 40.8, -74, 40.7, -73.9]
paris = ['paris', '13:00', 48.9, 2.2, 48.8, 2.3]
tokyo = ['tokyo', '05:00', 35.7, 139.8, 35.6, 139.7]
beijing = ['beijing', '06:00', 40.0, 116.0, 39.9, 116.1]
bangkok = ['bangkok', '07:00', 13.8, 100.4, 13.7, 100.5]
newdelhi = ['newdelhi', '08:00', 28.6, 76.8, 28.5, 76.9]
sidney = ['sidney', '04:00', -33.8, 150.6, -33.9, 150.7]
sanpaulo = ['sanpaulo', '17:00', -23.6, -47.0, -23.7, -46.9]
capetown = ['capetown', '12:00', -33.8, 18.3, -34.0, 18.5]


# In[ ]:


df = pd.DataFrame()


# In[ ]:


for area in tqdm([london, newyork, paris, tokyo, beijing, bangkok, newdelhi, sidney, sanpaulo, capetown]):

    # CDS API クライアントの初期化
    c = cdsapi.Client()

    # ダウンロードする年のリスト
    years = [str(year) for year in range(2019, 2024)]

    # データのダウンロード
    c.retrieve(
        'reanalysis-era5-land',
        {
            'variable': '2m_temperature',
            'format': 'grib',
            'year': years,
            'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'day': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'],
            'time': area[1],
            'area': area[2:],
        },
        'download.grib')

    # pygrib を使用してダウンロードしたデータファイルを開く
    grbs = pygrib.open('download.grib')

    # データをリストに格納
    temps = []
    for grb in grbs:
        data = grb.values
        temp_kelvin = data[0][0]  # データの範囲が小さすぎる場合、結果は1x1の配列になるため、最初の要素を取得
        temp_celsius = temp_kelvin - 273.15  # ケルビンを摂氏に変換
        temps.append(temp_celsius)
    df[area[0]] = temps


# In[ ]:


#ケープタウンを再取得。指定した座標では取得できる気温が少ないため。下から4行目を変更

for area in tqdm([capetown]):

    # CDS API クライアントの初期化
    c = cdsapi.Client()

    # ダウンロードする年のリスト
    years = [str(year) for year in range(2019, 2024)]

    # データのダウンロード
    c.retrieve(
        'reanalysis-era5-land',
        {
            'variable': '2m_temperature',
            'format': 'grib',
            'year': years,
            'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'day': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31'],
            'time': area[1],
            'area': area[2:],
        },
        'download.grib')

    # pygrib を使用してダウンロードしたデータファイルを開く
    grbs = pygrib.open('download.grib')

    # データをリストに格納
    temps = []
    for grb in grbs:
        data = grb.values
        temp_kelvin = data[0][-1]  # データの範囲が小さすぎる場合、結果は1x1の配列になるため、最初の要素を取得
        temp_celsius = temp_kelvin - 273.15  # ケルビンを摂氏に変換
        temps.append(temp_celsius)
    df[area[0]] = temps


# In[ ]:


df.to_csv("2m_temp_2019to2023.csv")


# In[ ]:





# In[ ]:




