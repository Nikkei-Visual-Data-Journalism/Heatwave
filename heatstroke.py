#熱中症の救急搬送患者数（総務省）
#https://www.fdma.go.jp/disaster/heatstroke/post3.html
#旧hot_weather
#（他のコードもすべて猛暑関連で後から認識しにくいので変更）

import tabula
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime, date

#PDFファイルのURLを取得
url = 'https://www.fdma.go.jp/disaster/heatstroke/post3.html'
r = requests.get(url)
text = r.text
soup = BeautifulSoup(text)

pattern = re.compile(r'.*heatstroke_sokuhouti.*\.pdf')
href_list = [a['href'] for a in soup.select('div > a[href]') if pattern.match(a['href'])]

def read_pdf(href):
    #URL
    parent_dir = 'https://www.fdma.go.jp'
    url = f"https://www.fdma.go.jp{href}"
    
    #PDFから表を取得
    dfs = tabula.read_pdf(url, stream=True, pages=1)
    df = dfs[0]
    
    #日付の列を探す
    for col in df.columns:
        try:
            df[df[col].str.contains('日付', na=False)].index.to_list()[0]
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

heatstroke = pd.DataFrame()

for href in set(href_list):
    weekly_data = read_pdf(href)
    heatstroke = pd.concat([heatstroke, weekly_data])

#重複削除
heatstroke = heatstroke[~heatstroke.duplicated(subset='date', keep='last')].set_index('date')
#日付の隙間を埋める
heatstroke = heatstroke.reindex(pd.date_range(heatstroke.index.min(), heatstroke.index.max()))
heatstroke = heatstroke.rename_axis('date').reset_index()

filepath = './data/heatstroke.csv'
heatstroke.to_csv(filepath, index=False)

#### change log####
#役所のPDFでカラムやインデックスを位置で決めうちするのはけっこう危険
#やや時間はかかりますが、列名などを特定して取得したほうがよいです
#データは数値は数値、日付は日付できれいにしておく