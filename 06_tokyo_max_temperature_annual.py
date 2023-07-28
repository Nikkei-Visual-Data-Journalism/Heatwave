#!/usr/bin/env python
# coding: utf-8

# # 東京の「d時点（前日）」の猛暑日（過去60年分、バーチャート作成）
# - [d時点]について。1963年〜2023年6月末までの東京（東京都）の日別最高気温データ'tokyo_maxtemp_byD_until202306.csv'(データソース：気象庁「過去の気象データ・ダウンロード」 'https://www.data.jma.go.jp/risk/obsdl/index.php#')
# - [d時点]について。2023年の7月以降は定期実行で自動取得（データソース：気象庁「過去の気象データ検索 > 日ごとの値」
# https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=7 )
# - 出力データ②（バーチャート用）:'tokyo_over30_count.csv'（東京の年間真夏日数）
# - 出力データ③（バーチャート用）:'tokyo_over35_count.csv'（東京の年間猛暑日数）

# In[1]:


import pandas as pd
import datetime
from datetime import datetime


# ### d時点のデータを取得

# #### 2023年の7月以降の最新データを取得

# In[10]:


# 現在の月を取得
today = datetime.now()
month = today.month


# In[11]:


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


# In[12]:


# データフレームのリストを連結
new_data = pd.concat(df_list)


# In[13]:


# 必要列を抽出
new_data = new_data.loc[:, [('日', '日','日','日'), ('気温(℃)','気温(℃)', '最高', '最高'), ('month', '', '', '')]]


# In[14]:


# 欠損値がある行を削除
new_data = new_data.dropna()


# In[15]:


# 列名を設定
new_data.columns = ['day','max', 'month']


# In[16]:


# 年列を作成
new_data['year'] = 2023

# month_day列を作成
new_data['month_day'] = new_data['month'].astype(str) + '/' + new_data['day'].astype(str)

# date列を作成
new_data['date'] = new_data['year'].astype(str) + '-' + new_data['month_day'].astype(str)
# date列を日付型に変換
new_data['date'] = pd.to_datetime(new_data['date'])

# month_data列を上書き
new_data['month_day'] = new_data['date'].dt.strftime('%m/%d')

# date列を文字列に戻す
new_data['date'] = new_data['date'].astype(str)


# In[17]:


new_data = new_data[['date','max','year','month','day','month_day']]


# #### 1963~2023年6月までの日別気温データと2023年7月以降データを結合

# In[19]:


# 過去データ読み込み
past_data = pd.read_csv('tokyo_maxtemp_byD_until202306.csv')


# In[20]:


# 過去データと最新データを結合
data = pd.concat([past_data, new_data], ignore_index=True)


# #### グラフ用に整形処理

# In[22]:


# 年毎に年間の猛暑日数をカウント
year_counts = data[data['max'] >= 35].groupby('year').size()

# max35_year_totalに年間の猛暑日数を代入する
data['max35_year_total'] = data['year'].map(year_counts)


# #### d日時点（今日の前日）のデータを抽出

# In[23]:


data.dtypes


# In[24]:


# date列を datetime.date 型に変換
data['date'] = pd.to_datetime(data['date']).dt.date


# In[25]:


# 1/1~前日までのデータを抽出

# 今日の日付の「日」「月」データを取得
today_day = pd.Timestamp.today().date().day
today_month = pd.Timestamp.today().date().month

# month列が1月からmonth未満の場合、対応するday列（その月の最小値から最大値の範囲）を全て取得
condition1 = data['month'].between(1, today_month - 1) & data['day'].between(data['day'].min(), data['day'].max())

# month列が今月の場合、1から今日の前日までの対応するday列データを取得（最高気温の最新データは前日までしか取得できない）
condition2 = (data['month'] == today_month) & data['day'].between(1, today_day - 1)

# 2つの条件のいずれかに該当するデータを抽出
ex_data = data.loc[condition1 | condition2]


# In[26]:


ex_data.groupby('year').size().unique()


# In[27]:


# 年毎の猛暑日のd日時点での合計値を算出
ex_data_max35 = ex_data[ex_data['max'] >= 35].groupby(['year','max35_year_total'])['month_day'].count().reset_index()

# d日時点での合計値としてtotal_on_date列に列名を変更
ex_data_max35.rename(columns={'month_day':'total_on_date'}, inplace=True)

# データ型をintに統一
ex_data_max35['max35_year_total'] = ex_data_max35['max35_year_total'].astype(int)

# 残り日数の列を作成
ex_data_max35['rem_days'] = ex_data_max35['max35_year_total'] - ex_data_max35['total_on_date'] 


# In[28]:


# 保存
ex_data_max35.to_csv('tokyo_maxtemp_data_until_now.csv', index=False)

