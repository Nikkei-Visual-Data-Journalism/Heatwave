#熱中症の救急搬送患者数（総務省）
#旧hot_weather
#（他のコードもすべて猛暑関連で後から認識しにくいので変更）
#ソース：消防庁
#毎週火曜（夕方？）に週次データをPDFで発表
#https://www.fdma.go.jp/disaster/heatstroke/post3.html

import pandas as pd
from datetime import datetime, date, timedelta
import tabula
import requests
from bs4 import BeautifulSoup
import re
import json

#1) 週次のPDFファイルのURLを取得する
##ポータルの中身をみる
url = 'https://www.fdma.go.jp/disaster/heatstroke/post3.html'
r = requests.get(url)
text = r.text
soup = BeautifulSoup(text, features="lxml")
##pdfのURLをいったん全部リストに入れる
pattern = re.compile(r'.*heatstroke_sokuhouti.*\.pdf')
href_list = [a['href'] for a in soup.select('div > a[href]') if pattern.match(a['href'])]

#2) pdfのURLから中身の表を取り出すファンクションを設定しておく
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

    #ほしいデータ＝「合計」の列を抜粋
    col_sum = [col for col in df.columns if '合計'in str(col)]
    data= df[col_sum].iloc[:,0].rename('熱中症患者数')
    data = pd.to_numeric(data.str.replace(',', ''), errors='coerce')
    data = data.reset_index().dropna(subset=['date'])
    return data

###毎回全部のURLをループするのは時間／安定性の面でよくないので
###過去分は蓄積しておき、新規分のみデータを取って積み上げる
#3) 前回までのデータ
filepath = './data/heatstroke.csv'
heatstroke = pd.read_csv(filepath, parse_dates=['date'])

#4)追加分のデータ取得
#前回までに取得済みのURL
with open('./data/heatstroke-pdf-list.json', 'r') as file:
    href_list_prev  = json.load(file)   
#新規の追加分URL
href_list_new = set(href_list) - set(href_list_prev)

#新規の追加分URLがあるときのみ
for href in href_list_new:
    try:
        weekly_data = read_pdf(href)
        heatstroke = pd.concat([heatstroke, weekly_data])
    except:
        pass
#重複削除
heatstroke = heatstroke[~heatstroke.duplicated(subset='date', keep='last')].set_index('date')
#日付の隙間を埋める（エラー防止）
heatstroke = heatstroke.reindex(pd.date_range(heatstroke.index.min(), heatstroke.index.max()))
heatstroke = heatstroke.rename_axis('date').reset_index()

#出力
#データ
heatstroke.to_csv(filepath, index=False)
#取得済みPDFのURL
with open('./data/heatstroke-pdf-list.json', 'w') as f:
    json.dump(href_list, f)

#### change log####
#役所のPDFでカラムやインデックスを位置で決めうちするのはけっこう危険
#やや時間はかかりますが、列名などを特定して取得したほうがよいです
#データは数値は数値、日付は日付形式できれいにしておく