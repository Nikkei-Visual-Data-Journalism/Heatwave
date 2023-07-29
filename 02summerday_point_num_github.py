# # 真夏日と猛暑日の地点数（全国）の取得コード
# 気象庁の「真夏日などの地点数（昨日まで）」のデータ
# https://www.data.jma.go.jp/obd/stats/etrn/view/summer.php?
# - GitHub用
# - 出力データは'japan_heatpoint_count.csv'

import pandas as pd
from datetime import datetime

# 現在の月を取得
month = datetime.today().month

# URLのベース部分を指定
base_url = 'https://www.data.jma.go.jp/obd/stats/etrn/view/summer.php?month='

#空のデータフレーム
df_list = []

# URLを生成して表示
for i in range(5, month + 1):
    url = base_url + str(i)
    print(url)
    df = pd.read_html(url)[2]
    df['month'] = i
    df_list.append(df)

# データフレームのリストを連結
data = pd.concat(df_list)

# マルチインデックスを解除
data.reset_index(drop=True, inplace=True)

# 列名を再設定
data.columns = ['day','真夏日', '猛暑日', 'month']

# month_day列を作成
data['month_day'] = data['month'].astype(str) + '/' + data['day'].astype(str)

data.set_index('month_day', inplace=True)

# flourish作成用にcsv保存
data.to_csv('./data/japan_heatpoint_count.csv')