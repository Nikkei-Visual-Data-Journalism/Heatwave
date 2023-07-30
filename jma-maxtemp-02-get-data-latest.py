#気象庁
#①最新の最高気温のデータを取得
#②過去のtsと統合してtimeseriesを更新

#https://www.data.jma.go.jp/stats/data/mdrr/docs/csv_dl_readme.html
#最新は1時間毎の更新（毎時00分の観測データを50分過ぎに更新）
#過去７日はウェブ上のデータは毎日5:00ごろ更新＋修正は13:00、19:00、翌日1:00ごろの更新で反映-->github上で30分遅れで取得しているものを呼び出す
#定期実行

import pandas as pd

#最新データの取得
url = 'https://www.data.jma.go.jp/stats/data/mdrr/tem_rct/alltable/mxtemsadext00_rct.csv'
data = pd.read_csv(url, encoding='Shift-JIS')

#日付
yyyymmdd = f"{data['現在時刻(年)'][0]}{data.loc[0,['現在時刻(月)','現在時刻(日)']].apply(lambda x: str(x).zfill(2)).sum()}"
yyyymmdd_dt = pd.to_datetime(yyyymmdd, format='%Y%m%d')

#最新データをcsvで出力
##ファイル名
filename = f"./data-maxtemp/daily-data/jma-maxtemp-{yyyymmdd}.csv"
##記載
data['date'] = yyyymmdd_dt
##csv
data.to_csv(filename, index=False)

#真夏日・猛暑日の数をかぞえる
rename_dic = {col:'maxtemp' for col in data.columns if '最高気温(℃)' in col}
data = data.rename(columns=rename_dic)

###計算
data['over15'] = data.maxtemp >= 15
data['over20'] = data.maxtemp >= 20
data['over25'] = data.maxtemp >= 25
data['over30'] = data.maxtemp >= 30
data['over35'] = data.maxtemp >= 35
data['over40'] = data.maxtemp >= 40
data['over45'] = data.maxtemp >= 45
data['over50'] = data.maxtemp >= 50
data['total'] = 1
data['null_values'] = data.maxtemp.isna()

###集計
heat_points_latest = data[['over15','over20','over25','over30','over35','over40','over45','over50','total','null_values']].sum()
heat_points_latest['date'] = yyyymmdd_dt

#過去分と統合
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-ts.csv"
##過去分を取得
heat_points = pd.read_csv(filename)
heat_points.date = pd.to_datetime(heat_points.date)

##統合して重複削除（新しく入ったほうを残す）
heat_points = pd.concat([heat_points, heat_points_latest.to_frame().T])
heat_points = heat_points.loc[~heat_points.duplicated(subset=['date'], keep='last')].reset_index(drop=True)
heat_points = heat_points.dropna(subset='date').sort_values(by='date')

##出力
heat_points.to_csv(filename, index=False)

#最終更新時刻を記録
##動的テキスト表示用（使えるかは未定）
update_log = f"{yyyymmdd_dt.strftime('%Y年%-m月%-d日')}{data['現在時刻(時)'][0]}時時点"
with open('./data-maxtemp/timeseries-data/update_log.txt', 'w') as f:
    f.write(update_log)