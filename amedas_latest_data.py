#amedasから最新の気象データを取得するコード

#dependencies
import requests
import pandas as pd
from datetime import datetime,timedelta

#data1: 地点情報
url = 'https://www.jma.go.jp/bosai/amedas/const/amedastable.json'
r = requests.get(url)
data1 = r.json()

#data2: amedasの最新気象データ
##最新の時刻
url = 'https://www.jma.go.jp/bosai/amedas/data/latest_time.txt'
r = requests.get(url)
latest_time = r.text
latest_time = datetime.strptime(latest_time, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y%m%d%H0000')

##最新のデータ
url = f"https://www.jma.go.jp/bosai/amedas/data/map/{latest_time}.json"
r = requests.get(url)
data2 = r.json()

#データ整形
##data1とdata2を統合
amedas_data = {key: {**data1.get(key, {}), **data2.get(key, {})} for key in set(data1) | set(data2)}
#dataframe
amedas = pd.DataFrame(amedas_data)
amedas = amedas.T.rename_axis('amdno').reset_index()

##geo-cordをととのえる
amedas[['lat','lon']] = amedas[['lat','lon']].applymap(lambda x: x[0] + x[1]/60)

##残りのリスト形式のデータから値のみ抽出
amedas = amedas.applymap(lambda x: x[0] if type(x)==list else x)

#色分け用
amedas.loc[(amedas.temp<0),'temp_color'] = '氷点下'
amedas.loc[(amedas.temp>=0)&(amedas.temp<5),'temp_color'] = '0〜5度以下'
amedas.loc[(amedas.temp>=5)&(amedas.temp<10),'temp_color'] = '5〜10度以下'
amedas.loc[(amedas.temp>=10)&(amedas.temp<15),'temp_color'] = '10〜15度以下'
amedas.loc[(amedas.temp>=15)&(amedas.temp<20),'temp_color'] = '15〜20度以下'
amedas.loc[(amedas.temp>=20)&(amedas.temp<25),'temp_color'] = '20〜25度以下'
amedas.loc[(amedas.temp>=25)&(amedas.temp<30),'temp_color'] = '25〜30度以下'
amedas.loc[(amedas.temp>=30)&(amedas.temp<35),'temp_color'] = '30〜35度以下'
amedas.loc[(amedas.temp>=35)&(amedas.temp<40),'temp_color'] = '35〜40度以下'
amedas.loc[(amedas.temp>=40),'temp_color'] = '40度以上'

#データ出力
###全部入り
amedas.to_csv('./data/amedas_latest_all.csv',encoding='utf-8-sig',index=False)

###tempのみ
amedas.dropna(subset=['temp']).to_csv('./data/amedas_latest_temp.csv',encoding='utf-8-sig',index=False)