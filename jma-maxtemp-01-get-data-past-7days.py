#気象庁
#過去7日間の最高気温のデータを取得するコード
#https://www.data.jma.go.jp/stats/data/mdrr/docs/csv_dl_readme.html
#ウェブ上のデータは毎日5:00ごろ更新＋修正は13:00、19:00、翌日1:00ごろの更新で反映
#定期実行

import pandas as pd
import re

#データを取得してファイル名に日付を入れて保存する
def get_previous_data(d):
    url = f'https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsadext0{d}.csv'
    data = pd.read_csv(url, encoding='Shift-JIS')

    #日付
    yyyymmdd = f"{data['観測時刻(年)'][0]}{data.loc[0,['観測時刻(月)','観測時刻(日)']].apply(lambda x: str(x).zfill(2)).sum()}"
    #ファイル名
    
    filename = f"./data-maxtemp/daily-data/jma-maxtemp-{yyyymmdd}.csv"
    #dataにも記載
    data['date'] = pd.to_datetime(yyyymmdd, format='%Y%m%d')
    #csvで出力
    data.to_csv(filename, index=False)
    return data

#実行
#集計（真夏・猛暑日を数える）
data_agg = pd.DataFrame()

###データ取得
for d in range(1, 8): 
    data = get_previous_data(d)
    ##ととのえる
    ##最高気温のデータのカラムを抽出
    ##（1日前＝昨日の~、2日前=一昨日の~、3日以上前=xx日の最高気温(℃)
    rename_dic = {col:'maxtemp' for col in data.columns if '日の最高気温(℃)' in col}
    data = data.rename(columns=rename_dic)
    ##統合
    data_agg = pd.concat([data_agg, data])

###計算
data_agg['over15'] = data_agg.maxtemp >= 15
data_agg['over20'] = data_agg.maxtemp >= 20
data_agg['over25'] = data_agg.maxtemp >= 25
data_agg['over30'] = data_agg.maxtemp >= 30
data_agg['over35'] = data_agg.maxtemp >= 35
data_agg['over40'] = data_agg.maxtemp >= 40
data_agg['over45'] = data_agg.maxtemp >= 45
data_agg['over50'] = data_agg.maxtemp >= 50
data_agg['total'] = 1
data_agg['null_values'] = data_agg.maxtemp.isna()

#集計df
heat_points_7days = data_agg.groupby(['date'])[['over15','over20','over25','over30','over35','over40','over45','over50','total','null_values']].sum().reset_index()

#過去分と統合
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-ts.csv"
##過去分を取得
heat_points = pd.read_csv(filename)
heat_points = pd.concat([heat_points,heat_points_7days])
##重複削除（新しく入ったほうを残す）
heat_points.date = pd.to_datetime(heat_points.date)
heat_points = heat_points.loc[~heat_points.duplicated(subset=['date'], keep='last')].reset_index(drop=True)
heat_points = heat_points.dropna(subset='date').sort_values(by='date')

##出力
heat_points.to_csv(filename, index=False)