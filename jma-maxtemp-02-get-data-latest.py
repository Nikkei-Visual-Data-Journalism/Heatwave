#気象庁
#①最新の最高気温のデータを取得
#②集計１：真夏日・猛暑日の観測地点数（全国）＝過去データ統合して更新
#③集計２：各都道府県の最高気温一覧＝過去データと統合して更新
#④集計３：各観測地点のきょうの最高気温（直近のみ）＝最新データに更新

#https://www.data.jma.go.jp/stats/data/mdrr/docs/csv_dl_readme.html
#最新は1時間毎の更新（毎時00分の観測データを50分過ぎに更新）
#過去７日はウェブ上のデータは毎日5:00ごろ更新＋修正は13:00、19:00、翌日1:00ごろの更新で反映-->github上で30分遅れで取得しているものを呼び出す
#定期実行

import pandas as pd

#観測地点の一覧
url = 'https://raw.githubusercontent.com/Nikkei-Visual-Data-Journalism/Heatwave/main/data-maxtemp/meta/points_list.csv'
points = pd.read_csv(url)

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
data.to_csv("./data-maxtemp/daily-data/jma-maxtemp-latest.csv")

#真夏日・猛暑日の数をかぞえる
rename_dic = {col:'maxtemp' for col in data.columns if '最高気温(℃)' in col}
data = data.rename(columns=rename_dic)

#計算（集計1, 2共通）
data['over30'] = data.maxtemp >= 30
data['over35'] = data.maxtemp >= 35
data['over40'] = data.maxtemp >= 40
data['total'] = 1
data['null_values'] = data.maxtemp.isna()
#追加データ（集計2用）
data['pref'] = data['観測所番号'].map(points.set_index(['観測所番号']).pref.to_dict())
data['capitol'] = data['観測所番号'].isin(points[points.capitol==1]['観測所番号']).astype(int)
#追加データ（集計3用）
data['name'] = data['観測所番号'].map(points.set_index('観測所番号').name.to_dict())

#集計1: 猛暑・真夏日の観測地点数（全国）
##最新分
heat_points_latest = data[['over30','over35','over40','total','null_values']].sum()
heat_points_latest['date'] = yyyymmdd_dt
##過去分
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-ts.csv"
heat_points = pd.read_csv(filename)
heat_points.date = pd.to_datetime(heat_points.date)
##統合
heat_points = pd.concat([heat_points, heat_points_latest.to_frame().T])
heat_points = heat_points.loc[~heat_points.duplicated(subset=['date'], keep='last')].reset_index(drop=True)
heat_points = heat_points.dropna(subset='date').sort_values(by='date')
##出力
heat_points.to_csv(filename, index=False)

#Flourish用
heat_points['year'] = heat_points['date'].dt.year
heat_points['date_x_axis'] = heat_points['date'].apply(lambda x: x.replace(year=2000))
heat_points['date_jp'] = heat_points['date'].dt.strftime('%Y年%-m月%-d日')
heat_points_f = heat_points.set_index(['date','year','date_x_axis','date_jp'])[['over30','over35']].rename_axis('category',axis=1).stack().rename('heat_pointss')
heat_points_f = heat_points_f.reset_index()
#出力
filename_f30 = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-over30-ts.csv"
filename_f35 = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-over35-ts.csv"
heat_points_f[heat_points_f.category=='over30'].to_csv(filename_f30, index=False)
heat_points_f[heat_points_f.category=='over35'].to_csv(filename_f35, index=False)

#集計2：真夏日・猛暑日の県別一覧表
##最新分
data_table = data.groupby(['date','pref'])[['maxtemp','over30','over35','over40']].max()
data_table_cap = data[data.capitol==1].set_index(['date','pref'])[['maxtemp','over30','over35','over40']].add_suffix('_capitol')
data_table = pd.concat([data_table, data_table_cap],axis=1).reset_index()
##過去分
filename = "./data-maxtemp/timeseries-data/jma-maxtemp-temp-by-pref-ts.csv"
past_table = pd.read_csv(filename)
##統合
data_table = pd.concat([past_table, data_table])
data_table['date'] = pd.to_datetime(data_table['date'], errors='coerce')
data_table = data_table.dropna(subset=['date'])
data_table['year'] = data_table['date'].dt.year
data_table = data_table[~data_table.duplicated(subset=['date','pref'],keep='last')]
data_table['sort_n'] = data_table.pref.map(points.set_index('pref').prec_no.to_dict())
data_table = data_table.sort_values(by=['date','sort_n']).reset_index(drop=True)
#True/False-->1/0に
cols = [col for col in data_table.columns if 'over' in col]
data_table[cols] = data_table[cols].astype(int)

#集計2-2: 
##年間＆前年同期の猛暑・真夏日をカウント
data_table_fullyear = data_table.groupby(['year','pref','sort_n'])[cols].sum()
data_table_ytd = data_table[data_table['date'].apply(lambda x: x.replace(year=2000))<=yyyymmdd_dt.replace(year=2000)]
data_table_ytd = data_table_ytd.groupby(['year','pref','sort_n'])[cols].sum()
data_table_y = pd.concat([data_table_fullyear, data_table_ytd.add_suffix('_ytd')],axis=1)
data_table_y = data_table_y.sort_index(level=[0,2]).reset_index(level='sort_n', drop=True).reset_index()
##年間を出力
filename_y = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-by-pref-ts.csv"
data_table_y.to_csv(filename_y,index=False)
##Flourish用のバックデータを更新
flourish = pd.DataFrame()
temps = {30:'真夏日', 35:'猛暑日'}
for key, val in temps.items():
    temp_df = data_table_y.set_index(['year','pref'])[[col for col in data_table_y if str(key) in col]]
    rename_dic = {
        f'over{key}':'heatpoints',
        f'over{key}_capitol':'heatpoints_capitol',
        f'over{key}_ytd':'heatpoints_ytd',
        f'over{key}_capitol_ytd':'heatpoints_capitol_ytd'
    }
    temp_df = temp_df.rename(columns=rename_dic)
    temp_df['temp'] = val
    flourish = pd.concat([flourish, temp_df])
flourish = flourish.reset_index(drop=False)
flourish['year'] = flourish['year'].astype(int)
flourish[f"{yyyymmdd_dt.strftime('%-m月%-d日')}時点"] = flourish.heatpoints_capitol_ytd
flourish['残りの期間'] = flourish.heatpoints_capitol - flourish.heatpoints_capitol_ytd
###東京都を一番上に表示
flourish['sort_n'] = flourish.pref.map(points.set_index('pref').prec_no.to_dict())
flourish.loc[flourish.pref=='東京都','sort_n'] = 1
flourish = flourish.sort_values(by=['year','sort_n'])
###Flourishを出力
filename_f = "./data-maxtemp/timeseries-data/jma-maxtemp-heatpoints-by-pref-flourish.csv"
flourish.to_csv(filename_f,index=False)

##県別一覧を出力
data_table = data_table.drop(['sort_n'],axis=1)
data_table.to_csv(filename, index=False)

#集計3: 最高気温の表
##最新分のみで計算
heinen = [col for col in data.columns if '平年' in col][0]
rank_df = data[['date','観測所番号','pref','name','maxtemp',heinen]]
rank_df = rank_df.rename(columns={'pref':'都道府県名','name':'地名','maxtemp':'最高気温',heinen:'平年差'})
rank_df['平年差_pos'] = rank_df.where(rank_df['平年差']>0)['平年差'].fillna(0)
rank_df['平年差_neg'] = rank_df.where(rank_df['平年差']<0)['平年差'].fillna(0)
rank_df = rank_df.sort_values(by=['最高気温'],ascending=False)
##出力
rank_df.to_csv('./data/maxtemp-ranking-latest.csv',index=False)

#最終更新時刻を記録
##動的テキスト表示用（使えるかは未定）
update_log = f"{yyyymmdd_dt.strftime('%Y年%-m月%-d日')}{data['現在時刻(時)'][0]}時時点"
with open('./data-maxtemp/timeseries-data/update_log.txt', 'w') as f:
    f.write(update_log)