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
r = requests.get('https://www.jma.go.jp/bosai/amedas/data/latest_time.txt')
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

amedas.to_csv('./data/amedas_latest_data.csv',encoding='utf-8-sig',index=False)