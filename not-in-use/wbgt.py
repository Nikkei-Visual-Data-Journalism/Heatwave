#暑さ指数（旧hot_index）

#環境省のサーバーの問題で定期実行できないので使用していない
#詳細はissue

#ソース：環境省熱中症予防サイト
#元データは毎時30分ごろ更新
#https://www.wbgt.env.go.jp/wbgt_data.php

import pandas as pd
from datetime import datetime, date
import requests

#実況値のデータを取得
yyyymm = date.today().strftime('%Y%m')
url = f'https://www.wbgt.env.go.jp/est15WG/dl/wbgt_all_{yyyymm}.csv'
wbgt = pd.read_csv(url)

#日時データ整形
wbgt['Time'] = wbgt['Time'].str.replace('24:00','0:00')
wbgt['date_dt'] = pd.to_datetime(wbgt['Date'] + ' ' + wbgt['Time'], format='%Y/%m/%d %H:%M')
wbgt['dt_popup']=wbgt.date_dt.dt.strftime('%-m月%-d日 %-H時時点')
wbgt = wbgt.drop(['Date','Time'],axis=1)

#longフォーマットに転換
wbgt = wbgt.set_index(['date_dt','dt_popup']).rename_axis('amdno',axis=1).stack().rename('wbgt').reset_index()
wbgt.amdno = wbgt.amdno.astype(int)

#最新分のみ切り出し
##iloc[-1]などはほぼ大丈夫ですが、絶対値で指定したほうがより安全
wbgt_latest = wbgt.loc[wbgt.date_dt==wbgt.date_dt.max()]


#地点情報を取得
##tableを固定で引っ張ると、観測地点の変更・追加などがあるとデータがおちてしまうので、
##元データを引っ張ったほうがベター(コードは少しだけ長くなりますが、jsonで軽いので）
url = 'https://www.jma.go.jp/bosai/amedas/const/amedastable.json'
r = requests.get(url)
data = r.json()

locations = pd.DataFrame.from_dict(data, orient='index').reset_index()
locations = locations.rename(columns={'index':'amdno'})
locations.amdno = locations.amdno.astype(int)
#lat longを整える
locations[['lat','lon']] = locations[['lat','lon']].applymap(lambda x: x[0] + x[1]/60)

#地点情報を最新データに追加
##how='left'
wbgt_latest = wbgt_latest.merge(locations[['amdno','lat','lon','kjName']], on='amdno', how='left')

#暑さ指数「日常生活に関する指針」
##指針の内容をテキストでアサイン
def guideline(value):
    if value >= 31:
        return '危険'
    elif value >= 28:
        return '厳重警戒'
    elif value >= 25:
        return '警戒'
    elif value >= 21:
        return '注意'
    else:
        return 'ほぼ安全'
wbgt_latest['guideline'] = wbgt_latest.wbgt.apply(guideline)

cols = ['Date','Time','amdno','wbgt','dt_popup','lat','long','kjName','guideline']
wbgt_latest = wbgt_latest.loc[:,cols]

wbgt_latest.to_csv("./data/wbgt.csv", index=False)