#!/usr/bin/env python
# coding: utf-8

# In[39]:


import pandas as pd
import datetime
import requests
import ssl
import urllib.request



# In[40]:


#黄田さんが取得済みでaltとlonがあるdf_location_dataと、環境省が公開している暑さ指数データを合体する
#暑さ指数データの地点数は841。df_location_dataの地点数が若干多く、841ある分に関して合体する
#df_tempdataは気温ではなく暑さ指数。名称間違えた


# In[41]:


url = 'https://raw.githubusercontent.com/hiroki-sakuragi/climate_change/main/amedastable.csv'
df_location_data = pd.read_csv(url)


# In[42]:


#現在の年、月を取得
#https://www.wbgt.env.go.jp/est15WG/dl/wbgt_all_202304.csv
#データ取得URLが上記のため、年と月を取得する必要あり
#月が一桁のときは07など0をいれる

year = datetime.datetime.now().year
month = datetime.datetime.now().month
formatted_month = f"{month:02d}"


# In[43]:


#データをダウンロード

url = f'https://www.wbgt.env.go.jp/est15WG/dl/wbgt_all_{year}{formatted_month}.csv'
df_tempdata = pd.read_csv(url)


# In[44]:


df_tempdata = df_tempdata.dropna()


# In[45]:


#データが更新された時刻を取得

time = df_tempdata.Time.iloc[-1]


# In[46]:


df_tempdata = df_tempdata.iloc[[-1]].T[2:].rename(columns ={df_tempdata.index[-1] : 'hot_index'}).reset_index()
df_tempdata = df_tempdata.rename(columns = {'index':'amdno'})
df_tempdata['time'] = time


# In[47]:


df_tempdata['amdno'] = df_tempdata['amdno'].astype(int)


# In[48]:


df_merge = pd.merge(df_tempdata, df_location_data, on = 'amdno')


# In[49]:


df_merge.to_csv("./data/hot_index.csv", index = False)




