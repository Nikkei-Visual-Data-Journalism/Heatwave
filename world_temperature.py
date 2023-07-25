#!/usr/bin/env python
# coding: utf-8

# In[38]:


import requests
import pandas as pd
import numpy as np
from datetime import datetime


# In[39]:


url = 'https://climatereanalyzer.org/clim/t2_daily/json/cfsr_world_t2_day.json'


# In[40]:


response = requests.get(url)


# In[41]:


data = response.json()


# In[42]:


df_data = pd.DataFrame(data)


# In[44]:


#flourishに読み込むデータ（df）はdate, year, tempで構成する

today = datetime.today().strftime('%Y-%m-%d')

dates = pd.date_range(start='1979-01-01', end=today)

# 月と日を取り出して文字列に変換し、連結する
month_day = dates.month.astype(str) + '/' + dates.day.astype(str)

# 年を取り出す
year = dates.year

# 新たなデータフレームを作成
df = pd.DataFrame({
    'date': month_day,
    'year': year
})


# In[47]:


#df_dataの下3行は使わないので削除する必要あり

df_data = df_data.iloc[:-3]


# In[49]:


temp = []


# In[50]:


df_data.data[0]


# In[52]:


#閏年でない年は、最後にnoneが入っているから取り除く必要あり

for i in range(len(df_data)):
    list_with_none = df_data.data[i]
    list_without_none = [x for x in list_with_none if x is not None]
    
#noneを取り除いたリストができたので、tempリストに集約（）
    
    for k in range(len(list_without_none)):
        temp.append(round(list_without_none[k], 2))


# In[53]:


#本日の日付までデータが更新されているわけではないため、tempの数とdfの行数は異なる
#なので足りない分、temp列をNaNで埋める

df['temp'] = pd.Series(np.nan, index = df.index)


# In[54]:


#あるだけtempデータを入れる

df.loc[df.index[:len(temp)], 'temp'] = temp


# In[55]:


df = df.dropna()


# In[56]:


df_without_229 = df[~df['date'].str.contains('^2/29$', regex=True)]


# In[57]:


df_without_229 = df_without_229[['temp', 'year', 'date']]


# In[59]:


df_without_229.to_csv("world_temperature.csv")


# In[ ]:





# In[ ]:





# In[ ]:




