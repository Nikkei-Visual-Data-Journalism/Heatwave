#熱中症の救急搬送患者数（総務省）
#https://www.fdma.go.jp/disaster/heatstroke/post3.html
#毎週火曜（夕方？）に週次データをPDFで発表

#旧hot_weather
#（他のコードもすべて猛暑関連で後から認識しにくいので変更）

import pandas as pd
from datetime import datetime, date, timedelta
import tabula
import requests
from bs4 import BeautifulSoup
import re

#PDFファイルのURLを取得
url = 'https://www.fdma.go.jp/disaster/heatstroke/post3.html'
r = requests.get(url)
text = r.text
soup = BeautifulSoup(text, features="lxml")

pattern = re.compile(r'.*heatstroke_sokuhouti.*\.pdf')
href_list = [a['href'] for a in soup.select('div > a[href]') if pattern.match(a['href'])]

def read_pdf(href):
    #URL
    parent_dir = 'https://www.fdma.go.jp'
    url = f"https://www.fdma.go.jp{href}"
    
    #PDFから表を取得
    dfs = tabula.read_pdf(url, stream=True, pages=1)
    df = dfs[0].reset_index(drop=True)
    
    #日付の列を探す
    for col in df.columns:
        try:
            idx = df[df[col].str.contains('日付', na=False)].index.to_list()[0]
            break
        except:
            pass
    
    #日付に変換
    df = df.rename(columns={col:'date'})
    df['date'] = df['date'].apply(lambda x: pd.to_datetime(f"{date.today().year}年{str(x).split(' ')[0]}", format='%Y年%m月%d日', errors='coerce'))
    df = df.set_index('date')
    
    #カラム名
    df.columns = df.iloc[idx+1].to_list()

    #「合計」の列を抜粋
    col_sum = [col for col in df.columns if '合計'in str(col)]
    data= df[col_sum].iloc[:,0].rename('熱中症患者数')
    data = pd.to_numeric(data.str.replace(',', ''), errors='coerce')
    data = data.reset_index().dropna(subset=['date'])
    return data

#過去分のデータを取得
filepath = './data/heatstroke.csv'
heatstroke = pd.read_csv(filepath, parse_dates=['date'])
#最終更新日
date_latest = heatstroke.date.max() - timedelta(days=6)
date_latest = int(date_latest.strftime('%Y%m%d'))
#最終更新日以降のファイルURLのみ取得
href_list = [href for href in href_list if int(re.search(r'(\d{8})\.pdf', href).group(1)) > date_latest]

#追加があるときのみ
if len(href_list)>0:
    #追加分のデータ取得
    for href in set(href_list):
        weekly_data = read_pdf(href)
        heatstroke = pd.concat([heatstroke, weekly_data])
    #重複削除
    heatstroke = heatstroke[~heatstroke.duplicated(subset='date', keep='last')].set_index('date')
    #日付の隙間を埋める
    heatstroke = heatstroke.reindex(pd.date_range(heatstroke.index.min(), heatstroke.index.max()))
    heatstroke = heatstroke.rename_axis('date').reset_index()
    print('Updated')
else:
    print('No updates')
    pass
           
#heatstroke.to_csv(filepath, index=False)

#### change log####
#役所のPDFでカラムやインデックスを位置で決めうちするのはけっこう危険
#やや時間はかかりますが、列名などを特定して取得したほうがよいです
#データは数値は数値、日付は日付できれいにしておく