#気象庁
#最新の最高気温のデータを取得
#集計1：真夏日・猛暑日の観測地点数（全国）＝過去データ統合して更新
#集計2：各都道府県の最高気温一覧＝過去データと統合して更新
#集計3: 年間＆前年同期の猛暑・真夏日をカウント
#集計4：各観測地点のきょうの最高気温（直近のみ）＝最新データに更新

#https://www.data.jma.go.jp/stats/data/mdrr/docs/csv_dl_readme.html
#最新は1時間毎の更新（毎時00分の観測データを50分過ぎに更新）
#過去７日はウェブ上のデータは毎日5:00ごろ更新＋修正は13:00、19:00、翌日1:00ごろの更新で反映-->github上で30分遅れで取得しているものを呼び出す
#定期実行

import pandas as pd

#観測地点の一覧
url = 'https://raw.githubusercontent.com/Nikkei-Visual-Data-Journalism/Heatwave/main/data-maxtemp/meta/points_list.csv'
points = pd.read_csv(url)
points_dic = points.set_index('pref').prec_no.to_dict()

#最新データの取得
url = 'https://www.data.jma.go.jp/stats/data/mdrr/tem_rct/alltable/mxtemsadext00_rct.csv'
data = pd.read_csv(url, encoding='Shift-JIS')

#日付
yyyymmdd = f"{data['現在時刻(年)'][0]}{data.loc[0,['現在時刻(月)','現在時刻(日)']].apply(lambda x: str(x).zfill(2)).sum()}"
yyyymmdd_dt = pd.to_datetime(yyyymmdd, format='%Y%m%d')
data['date'] = yyyymmdd_dt

#最新データをcsvで出力
##ファイル名
filename = f"./data-maxtemp/daily-data/jma-maxtemp-{yyyymmdd}.csv"
data.to_csv(filename, index=False)
data.to_csv("./data-maxtemp/daily-data/jma-maxtemp-latest.csv")

#真夏日・猛暑日の数をかぞえる
rename_dic = {col:'maxtemp' for col in data.columns if '最高気温(℃)' in col}
data = data.rename(columns=rename_dic)
data.maxtemp = data.maxtemp.astype(float)

#計算（集計1, 2共通）
data['over30'] = data.maxtemp >= 30
data['over35'] = data.maxtemp >= 35
data['over40'] = data.maxtemp >= 40
data['total'] = 1
data['null_values'] = data.maxtemp.isna()
#追加データ（集計2用）
data['pref'] = data['観測所番号'].map(points.set_index(['観測所番号']).pref.to_dict())
data['capitol'] = data['観測所番号'].isin(points[points.capitol==1]['観測所番号']).astype(int)
data['year'] = data.date.dt.year
#追加データ（集計3用）
data['name'] = data['観測所番号'].map(points.set_index('観測所番号').name.to_dict())


#集計1: 猛暑・真夏日の観測地点数（全国）
##最新分
heatpoints_latest = data[['over30','over35','over40','total','null_values']].sum()
heatpoints_latest['date'] = yyyymmdd_dt
##過去分
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-ts.csv"
heatpoints = pd.read_csv(filename)
heatpoints.date = pd.to_datetime(heatpoints.date)
##統合
heatpoints = pd.concat([heatpoints, heatpoints_latest.to_frame().T])
heatpoints = heatpoints.loc[~heatpoints.duplicated(subset=['date'], keep='last')].reset_index(drop=True)
heatpoints = heatpoints.dropna(subset='date').sort_values(by='date')
##出力
heatpoints.to_csv(filename, index=False)

#集計1: 猛暑・真夏日の観測地点数（全国）、Flourish用
#日付の抜け漏れを補正・カラム名など日本語に
dates = pd.date_range(heatpoints.date.min(),heatpoints.date.max())
dates = dates[dates.month.isin(range(5, 11))]
heatpoints_f = heatpoints.set_index('date').reindex(dates).rename_axis('date')
heatpoints_f['date_jp'] = heatpoints_f.index.strftime('%Y年%-m月%-d日')
heatpoints_f['year'] = heatpoints_f.index.strftime('%Y年')
heatpoints_f = heatpoints_f.rename(columns={'over30':'真夏日','over35':'猛暑日','over40':'酷暑日'}).reset_index()
heatpoints_f = heatpoints_f.sort_values(by=['year','date'], ascending=[False, True])
#出力
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-flourish.csv"
heatpoints_f.to_csv(filename, index=False)

#集計2：真夏日・猛暑日の県別一覧表
##最新分
by_pref_cap = data[data.capitol==1].groupby(['date','year','pref'])[['maxtemp','over30','over35','over40']].max().add_suffix('_capitol')
by_pref = data.groupby(['date','year','pref'])[['maxtemp','over30','over35','over40']].max()
by_pref = pd.concat([by_pref, by_pref_cap],axis=1).reset_index()
##過去分
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-by-pref-daily.csv"
by_pref_prev = pd.read_csv(filename, parse_dates=['date'])
#統合
by_pref = pd.concat([by_pref_prev, by_pref]).dropna(subset=['date'])
by_pref = by_pref[~by_pref.duplicated(subset=['date','pref'], keep='last')]
by_pref.loc[:,'over30':] = by_pref.loc[:,'over30':].astype(bool)
#出力
by_pref.to_csv(filename, index=False)

#集計3: 年間＆前年同期の猛暑・真夏日をカウント
cols = ['over30','over30_capitol', 'over35', 'over35_capitol', 'over40','over40_capitol']
by_pref['sort_n'] = by_pref.pref.map(points_dic)
#年間
by_pref_y = by_pref.groupby(['year','pref','sort_n'])[cols].sum()
#前年同期
by_pref_ytd = by_pref[by_pref['date'].apply(lambda x: x.replace(year=2000))<=yyyymmdd_dt.replace(year=2000)]
by_pref_ytd = by_pref_ytd.groupby(['year','pref','sort_n'])[cols].sum().add_suffix('_ytd')
#統合
by_pref_y = pd.concat([by_pref_y, by_pref_ytd],axis=1)
#並び順ソート
by_pref_y = by_pref_y.sort_index(level=['year','sort_n']).reset_index()
##年間を出力
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-by-pref-yearly.csv"
by_pref_y.drop('sort_n', axis=1).to_csv(filename,index=False)

#集計3: 年間＆前年同期の猛暑・真夏日をカウント(Flourish用に整形)
over30 = by_pref_y.set_index(['year','pref','sort_n'])[['over30_capitol','over30_capitol_ytd']]
over35 = by_pref_y.set_index(['year','pref','sort_n'])[['over35_capitol','over35_capitol_ytd']]
over40 = by_pref_y.set_index(['year','pref','sort_n'])[['over40_capitol','over40_capitol_ytd']]
over30['temp'] = '真夏日'
over35['temp'] = '猛暑日'
over40['temp'] = '酷暑日'
by_pref_f = pd.concat([over30, over35, over40]).sort_index(axis=1).reset_index()
#東京を上に表示する
by_pref_f.loc[by_pref_f.pref=='東京都','sort_n'] = 1
by_pref_f = by_pref_f.sort_values(by=['year','sort_n'])
#年
by_pref_f.year = by_pref_f.year.astype(int)
#出力
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-by-pref-flourish.csv"
by_pref_f.to_csv(filename,index=False)

#集計4: 最高気温の表
##最新分のみで計算
rank_df = data[['date','観測所番号','pref','name','maxtemp']]
rank_df = rank_df.rename(columns={'pref':'都道府県名','name':'地名','maxtemp':'最高気温'})
rank_df = rank_df.sort_values(by=['最高気温'],ascending=False)
##出力
filename = './data/maxtemp-ranking-latest.csv'
rank_df.to_csv(filename,index=False)

#最終更新時刻を記録
##動的テキスト表示用（使えるかは未定）
update_log = f"{yyyymmdd_dt.strftime('%Y年%-m月%-d日')}{data['現在時刻(時)'][0]}時時点"
with open('./data-maxtemp/timeseries-data/update_log.txt', 'w') as f:
    f.write(update_log)
