#!/usr/bin/env python
# coding: utf-8

# # 東京気温データ
# - github用
# - 1963〜2022年（6月1日〜9月31日）の東京（気象庁）の気温(データソース：気象庁「過去の気象データ・ダウンロード」https://www.data.jma.go.jp/risk/obsdl/index.php)
# - 2023年は6月分のデータをダウンロードし、上記過去分と結合してcsvに（github_data/1963_2022_all_202306only.csv）
# - 2023年の7月以降は自動取得（データソース：気象庁「過去の気象データ検索 > 日ごとの値」
# https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=7 )
# - 出力データ①（ヒートマップ用）：'tokyo_max_temp.csv'（東京過去70年分の最高気温）
# - 出力データ②（棒グラフ用）:'tokyo_over30_count.csv'（6月以降の東京の真夏日数）
# - 出力データ③（棒グラフ用）:'tokyo_over35_count.csv'（6月以降の東京の猛暑日数）

# In[1]:


import pandas as pd
import datetime
from datetime import datetime


# In[2]:


# 現在の月を取得
month = datetime.today().month


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


# In[5]:


# データフレームのリストを連結
new_data = pd.concat(df_list)


# In[6]:


# 必要列を抽出
new_data = new_data.loc[:, [('日', '日','日','日'), ('気温(℃)','気温(℃)', '最高', '最高'), ('month', '', '', '')]]


# In[8]:


# 欠損値がある行を削除
new_data = new_data.dropna()


# In[9]:


# 列名を設定
new_data.columns = ['day','max', 'month']


# In[10]:


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


# In[11]:


new_data = new_data[['date','max','year','month','day','month_day']]


# ### 過去データ（1964〜2022年の6月1日〜9月31日と2023年6月分）と最新データを結合

# In[13]:


# 過去データ読み込み
past_data = pd.read_csv('Heatwave/1963_2022_all_202306only.csv')


# In[14]:


# 過去データと最新データを結合
data = pd.concat([past_data, new_data], ignore_index=True)


# In[471]:


# flourish用に日付データを作成
data['month_day_flourish'] = data['month'].astype(str) + '/' + data['day'].astype(str)


# In[483]:


# githubのHeatwave/dataに保存
data.to_csv('Heatwave/data/tokyo_max_temp.csv')


# In[ ]:





# ### 東京6/1以降直近までで、猛暑日と真夏日の数を時系列比較

# In[15]:


# 今日の日付の「日」データを取得
today_day = pd.Timestamp.today().date().day
today_month = pd.Timestamp.today().date().month


# In[16]:


# 6/1~前日までのデータを抽出

# 6月よりあとの月かつmonth未満の場合、対応するday列（その月の最小値から最大値の範囲）を全て取得
condition1 = data['month'].between(6, today_month - 1) & data['day'].between(data['day'].min(), data['day'].max())

# monthが今月の場合、1から最新日前日までの対応するday列データを取得（最高気温の最新データは前日までしか取得できない）
condition2 = (data['month'] == today_month) & data['day'].between(1, today_day - 1)

# 2つの条件のいずれかに該当するデータを抽出
ex_data = data.loc[condition1 | condition2]


# In[17]:


# date列をインデックスに設定
ex_data.set_index('date', inplace=True)


# In[18]:


# 年ごとの真夏日の数
ex_data_30 = ex_data[ex_data['max'] >= 30]
year_counts_30 = ex_data_30['year'].value_counts() #年ごとの真夏日の数をカウント

# Github用に保存
year_counts_30.to_csv('Heatwave/data/tokyo_over30_count.csv')


# ### 2023年、真夏日の数は過去最高ペースで増えている

# In[488]:


# 年ごとの猛暑日の数
ex_data_35 = ex_data[ex_data['max'] >= 35]
year_counts_35 = ex_data_35['year'].value_counts()

# flourish用に保存
year_counts_35.to_csv('Heatwave/data/tokyo_over35_count.csv')

