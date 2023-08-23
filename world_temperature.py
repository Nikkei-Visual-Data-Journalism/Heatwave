import requests
import pandas as pd
from datetime import datetime

#データ取得
url = 'https://climatereanalyzer.org/clim/t2_daily/json/cfsr_world_t2_day.json'
response = requests.get(url)
data = response.json()

#不要データをおとす
##{'name': 'yyyy'}なので、'name'に数字（'yyyy'）以外が入っているものを除外
##これで末日にある年間データ以外の不要行（1979-2000 mean, plus 2σ, minus 2σの集計）が除外される
##iloc[:-3]は不要行が末尾以外に移動／増減した場合にうまくいかなくなるのであらかじめ予防できるエラーは防ぐ
data = [{**d} for d in data if d['name'].isdigit()]

#jsonデータをdfに
##dropna()で閏年でない年の末尾についていたnaはなくなる
##dataframeの名前はなるべくdf以外をつかう
world_temp = pd.json_normalize(data, 'data',['name'])
world_temp = world_temp.rename(columns={0:'temp', 'name':'year'}).dropna()

#日付を入れる
##for loopを使うより、元データの数を合わせて日付を入れたほうが速い
world_temp['date'] = pd.date_range(start='1979-01-01', periods=len(world_temp), freq='D')
#popup表示用のテキスト
world_temp['date_popup'] = world_temp.date.dt.strftime('%Y年%-m月%-d日')
##x軸描画用
world_temp['date_x_axis'] = world_temp.date.apply(lambda x: x.replace(year=2000)).dt.strftime('%Y-%m-%d')

#並び順をととのえる
world_temp = world_temp.loc[:,['date','date_popup','date_x_axis','year','temp']]

#出力
##dataフォルダに
world_temp.to_csv("./data/world_temperature.csv", index = False)
