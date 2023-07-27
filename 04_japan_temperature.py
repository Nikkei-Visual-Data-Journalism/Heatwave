#!/usr/bin/env python
# coding: utf-8

# # 東京気温データ（過去70年間）
# - 1963〜2022年（6月1日〜9月31日）の東京（気象庁）の気温(データソース：気象庁「過去の気象データ・ダウンロード」https://www.data.jma.go.jp/risk/obsdl/index.php)
# - 2023年は6/1〜6/30のデータを同様にダウンロードし、過去分と結合しcsv化（github_data/1964_2022_all_202306only.csv）
# - 2023年の7/1以降は自動取得に切り替え（データソース：気象庁「過去の気象データ検索 > 日ごとの値
# https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=7）

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import re
import japanize_matplotlib
import numpy as np
import seaborn as sns
import datetime
from datetime import datetime


# In[2]:


# 現在の月を取得
month = datetime.today().month
month


# In[3]:


# 気象庁から今年7月以降の気温データを読み込み

# URLのベース部分を指定
base_url = 'https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month='

#空のデータフレーム
df_list = []

# URLを生成して表示
for i in range(7, month + 1):
    url = base_url + str(i) #base_urlの最後の数字を入れ替え
    print(url)
    df = pd.read_html(url)[0]
    df['month'] = i
    df_list.append(df)
    
df_list[0]


# In[4]:


# データフレームのリストを連結
new_data = pd.concat(df_list)


# In[5]:


new_data.columns


# In[6]:


new_data.dtypes


# In[7]:


# 必要列を抽出
new_data = new_data.loc[:, [('日', '日','日','日'), ('気温(℃)','気温(℃)', '最高', '最高'), ('month', '', '', '')]]


# In[8]:


# 欠損値がある行を削除
new_data = new_data.dropna()
new_data


# In[9]:


# 列名を設定
new_data.columns = ['day','max', 'month']


# In[10]:


new_data


# In[11]:


# 年列を作成
new_data['year'] = 2023

# month_day列を作成
new_data['month_day'] = new_data['month'].astype(str) + '-' + new_data['day'].astype(str)

# date列を作成
new_data['date'] = new_data['year'].astype(str) + '-' + new_data['month_day'].astype(str)
# date列を日付型に変換
new_data['date'] = pd.to_datetime(new_data['date'])

# month_data列を上書き
new_data['month_day'] = new_data['date'].dt.strftime('%m-%d')

# date列を文字列に戻す
new_data['date'] = new_data['date'].astype(str)


# In[12]:


new_data = new_data[['date','max','year','month','day','month_day']]


# In[13]:


new_data.head()


# In[14]:


new_data.dtypes


# ### 過去データ（1963〜2022年の6月1日〜9月31日と2023年6月分）と結合

# In[15]:


# 過去データ読み込み
past_data = pd.read_csv('Heatwave/1963_2022_all_202306only.csv')
past_data


# In[16]:


past_data.dtypes


# In[17]:


# 過去データと最新データを結合
data = pd.concat([past_data, new_data], ignore_index=True)
data


# In[18]:


print(len(past_data))
print(len(new_data))
print(len(data))


# In[19]:


# 各列の欠損値数
data.isnull().sum()


# In[20]:


# flourish用に日付データを作成
data['month_day_flourish'] = data['month'].astype(str) + '/' + data['day'].astype(str)


# In[21]:


# flourish用に保存
data.to_csv('Heatwave/data/最高気温_1963_2022_all_2023_latest.csv')


# In[ ]:





# In[ ]:





# ## 描画

# In[22]:


# 最高気温
max_temp = data.pivot_table(values='max', index='year', columns='month_day')

# ヒートマップを描画
plt.figure(figsize=(10, 6))
sns.heatmap(max_temp, cmap='coolwarm', annot=False, fmt='g', linewidths=0.5)
plt.title('最高気温')
plt.xlabel('')
plt.ylabel('')


# 保存
# plt.savefig('output_data/最高気温_1964_2023.jpg')


# In[23]:


# 最高気温が３５℃以上の日を猛暑日、３０℃以上の日を真夏日、２５℃以上の日を夏日
# 猛暑日
max_temp = data.pivot_table(values='max', index='year', columns='month_day')

# カスタムカラーマップの作成
colors = ["white", "red"]  # より赤い色を追加
cmap_custom = mcolors.LinearSegmentedColormap.from_list("", colors)

# ヒートマップを描画
plt.figure(figsize=(10, 6))
sns.heatmap(max_temp, cmap=cmap_custom, annot=False, fmt='g', linewidths=0.5, vmin=35)
# sns.heatmap(data, cmap='Red', annot=True, fmt='d', cbar=False)
plt.title('猛暑日 最高気温35℃以上')
# plt.xlabel('')
plt.ylabel('年')


# In[24]:


# 最高気温が３５℃以上の日を猛暑日、３０℃以上の日を真夏日、２５℃以上の日を夏日
# 真夏日
max_temp = data.pivot_table(values='max', index='year', columns='month_day')

# ヒートマップを描画
plt.figure(figsize=(10, 6))
sns.heatmap(max_temp, cmap='Reds', annot=False, fmt='g', linewidths=0.5, vmin=30)
plt.title('真夏日 最高気温30℃以上')
plt.xlabel('')
plt.ylabel('')

# 保存
# plt.savefig('output_data/真夏日_1964_2023_heatmap.jpg')


# ### 東京6/1以降直近までのデータで、猛暑日と真夏日の数を時系列比較

# In[25]:


# 今日の日付の「日」データを取得
today_day = pd.Timestamp.today().date().day
today_month = pd.Timestamp.today().date().month
today_month


# In[26]:


# 6/1~前日までのデータを抽出

# 6月よりあとの月かつmonth未満の場合、対応するday列（その月の最小値から最大値の範囲）を全て取得
condition1 = data['month'].between(6, today_month - 1) & data['day'].between(data['day'].min(), data['day'].max())

# monthが今月の場合、1から最新日前日までの対応するday列データを取得（最高気温の最新データは前日までしか取得できない）
condition2 = (data['month'] == today_month) & data['day'].between(1, today_day - 1)

# 2つの条件のいずれかに該当するデータを抽出
ex_data = data.loc[condition1 | condition2]
ex_data


# In[27]:


# データ数各年揃ってる？
ex_data['year'].value_counts()


# In[28]:


# date列をインデックスに設定
ex_data.set_index('date', inplace=True)


# In[29]:


# 年ごとの真夏日の数
ex_data_30 = ex_data[ex_data['max'] >= 30]
year_counts_30 = ex_data_30['year'].value_counts() #年ごとの真夏日の数をカウント
sorted_years = sorted(year_counts_30.index)  # 年を昇順にソート

plt.figure(figsize=(6, 4))
plt.bar(sorted_years, year_counts_30[sorted_years])
plt.xticks(rotation=45, ha='right')  # x軸のラベルを斜めに表示
plt.title('東京　6/1以降の真夏日の数')
plt.xlabel('')
plt.ylabel('')

# 保存
# plt.savefig('output_data/真夏日_1964_2023_untill_resent_data.png')

# flourish用に保存
year_counts_30.to_csv('Heatwave/data/東京_真夏日_1963_2023_Jly1_to_latest_bar.csv')


# ### 2023年、真夏日の数は過去最高ペースで増えている

# In[30]:


# 年ごとの猛暑日の数
ex_data_35 = ex_data[ex_data['max'] >= 35]
year_counts_35 = ex_data_35['year'].value_counts()
sorted_years = sorted(year_counts_35.index)  # 年を昇順にソート

plt.figure(figsize=(6, 4))
plt.bar(sorted_years, year_counts_35[sorted_years])
plt.xticks(rotation= 45, ha='right')  # x軸のラベルを斜めに表示
plt.title('東京　6/1以降の猛暑日の数')
plt.xlabel('')
plt.ylabel('')


# 保存
# plt.savefig('output_data/猛暑日_1964_2023_untill_resent_data.png')

# flourish用に保存
year_counts_35.to_csv('Heatwave/data/東京_猛暑日_1963_2023_Jly1_to_latest_bar.csv')


# In[ ]:




