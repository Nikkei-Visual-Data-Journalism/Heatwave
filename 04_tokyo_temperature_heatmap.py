# # 東京の夏の最高気温（ヒートマップ作成）
# - github用
# - 1963〜2022年（6月1日〜9月31日）の東京（東京都）の気温(データソース：気象庁「過去の気象データ・ダウンロード」https://www.data.jma.go.jp/risk/obsdl/index.php)
# - 2023年は6月分のデータをダウンロードし、上記過去分と結合してcsvに（github_data/1963_2022_all_202306only.csv）
# - 2023年の7月以降は自動取得（データソース：気象庁「過去の気象データ検索 > 日ごとの値」
# https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=7 )
# - 出力データ①（ヒートマップ用）：'tokyo_max_temp.csv'（東京過去70年分の最高気温）

import pandas as pd
import datetime
from datetime import datetime

# 現在の月を取得
month = datetime.today().month

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

# データフレームのリストを連結
new_data = pd.concat(df_list)

# 必要列を抽出
new_data = new_data.loc[:, [('日', '日','日','日'), ('気温(℃)','気温(℃)', '最高', '最高'), ('month', '', '', '')]]

# 欠損値がある行を削除
new_data = new_data.dropna()

# 列名を設定
new_data.columns = ['day','max', 'month']

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

new_data = new_data[['date','max','year','month','day','month_day']]


# ### 過去データ（1964〜2022年の6月1日〜9月31日と2023年6月分）と最新データを結合

# 過去データ読み込み
past_data = pd.read_csv('./data-tokyo/1963_2022_all_202306only.csv')

# 過去データと最新データを結合
data = pd.concat([past_data, new_data], ignore_index=True)

# flourish用に日付データを作成
data['month_day_flourish'] = data['month'].astype(str) + '/' + data['day'].astype(str)

# 保存
data.to_csv('./data-tokyo/tokyo_max_temp.csv')