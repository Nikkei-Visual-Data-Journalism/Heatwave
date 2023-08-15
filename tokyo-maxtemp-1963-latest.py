# # 東京の夏の最高気温（ヒートマップ作成用）
#旧04_tokyo_temperature_heatmap.py

#####過去データ#########################################
# - 1963〜2022年（6月1日〜9月31日）の東京（東京都）の気温(データソース：気象庁「過去の気象データ・ダウンロード」https://www.data.jma.go.jp/risk/obsdl/index.php)
# - 2023年は6月分のデータをダウンロードし、上記過去分と結合してcsvに（github_data/1963_2022_all_202306only.csv）
######################################################

#####最新データ#########################################
# - 2023年の7月以降はjma-maxtempから取得した県別データから東京都を抜粋
# - 出力データ（ヒートマップ用）：'tokyo_max_temp.csv'（東京過去70年分の最高気温）
######################################################

import pandas as pd
from datetime import datetime, date

# 過去データ
filepath = './data-tokyo/1963_2022_all_202306only.csv'
past_data = pd.read_csv(filepath, parse_dates =['date'])

#最新データ
filepath = './data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-by-pref-daily.csv'
latest = pd.read_csv(filepath, parse_dates=['date'])
#必要箇所を抜粋
latest = latest.loc[(latest.pref=='東京都'),['date','maxtemp_capitol','year']]
latest = latest.rename(columns={'maxtemp_capitol':'max'})

#統合
tokyo = pd.concat([past_data, latest])
#重複削除
tokyo = tokyo[~tokyo.duplicated(subset=['date'], keep='last')]

#日付
#（不要分もあるがあとで整理）
#念のため抜け漏れを埋める
dates_ = pd.date_range(tokyo.date.min(), tokyo.date.max())
dates_ = [d for d in dates_ if (d.month>5) & (d.month<10)]
tokyo = tokyo.set_index('date').reindex(dates_).rename_axis('date').reset_index()
#フォーマット
tokyo.month = tokyo.date.dt.month
tokyo.day = tokyo.date.dt.day
tokyo.month_day = tokyo.date.dt.strftime('%m-%d')
tokyo['month_day_flourish'] = tokyo.date.dt.strftime('%-m/%-d')

# 保存
tokyo.to_csv('./data-tokyo/tokyo_max_temp.csv')