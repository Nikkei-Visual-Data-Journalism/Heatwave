#気象庁
#過去7日間の最高気温のデータを取得するコード
#https://www.data.jma.go.jp/stats/data/mdrr/docs/csv_dl_readme.html
#ウェブ上のデータは毎日5:00ごろ更新＋修正は13:00、19:00、翌日1:00ごろの更新で反映

import pandas as pd

def get_previous_data(d):
    url = f'https://www.data.jma.go.jp/obd/stats/data/mdrr/tem_rct/alltable/mxtemsadext0{d}.csv'
    data = pd.read_csv(url, encoding='Shift-JIS')

    file_dir = './data-ts-maxtemp/'
    file_name = f"jma-maxtemp-{data['観測時刻(年)'][0]}{data.loc[0,['観測時刻(月)','観測時刻(日)']].apply(lambda x: str(x).zfill(2)).sum()}.csv"

    data.to_csv(file_dir+file_name, index=False)
    
for d in range(1, 8):
    get_previous_data(d)