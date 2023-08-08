##世界の都市の気温変化のビジュアルを作成する
import pandas as pd
import altair as alt

#import requests
#from bs4 import BeautifulSoup
#from tqdm import tqdm
#import time
#import numpy as np

cities = {
    'london': 'ロンドン',
    'newyork': 'ニューヨーク', 
    'paris': 'パリ', 
    'tokyo': '東京', 
    'beijing': '北京', 
    'bangkok': 'バンコク', 
    'newdelhi': 'ニューデリー', 
    'sidney': 'シドニー', 
    'sanpaulo': 'サンパウロ', 
    'capetown': 'ケープタウン'
    }

#過去データ
filepath = './data-world-cities/2m_temp_1950to1954.csv'
df_past = pd.read_csv(filepath, index_col = 0)
df_past = df_past.rename(columns=cities)
df_past = df_past[cities.values()]

#現在のデータ
filepath = './data-world-cities/2m_temp_2019to2023.csv' 
df_present = pd.read_csv(filepath, index_col = 0)
df_present = df_present.rename(columns=cities)
df_present = df_present[cities.values()]

#描画
#線を引き、過去と現在でopacityを変えている
#作成したチャート10個の搬入先
charts = []

# データの生成
for city in cities.values():
    
    past = df_past.copy()[[city]]
    past['time'] = 'past'
    present = df_present.copy()[[city]]
    present['time'] = 'present'

    data = pd.concat([past, present]).dropna()

    #チャートの生成（エリアと境界線に分ける）
    def create_chart(data, time):
        color = 'gray' if time == 'past' else 'red'
        opacity = 0.2 if time == 'past' else 0.5
        
        chart_area = alt.Chart(data[data['time'] == time]).transform_density(
            density=city,
            as_=[city, 'density'],
        ).mark_area(opacity=opacity).encode(
            x=alt.X(f"{city}:Q", axis=alt.Axis(values = [-20, -10, 0, 10, 20, 30, 40]), scale=alt.Scale(domain=[-20, 50]), title=" (℃)"),
            y=alt.Y("density:Q", axis=None),
            color=alt.value(color),
        ).properties(
            width=150,
            height=80,
        )

    #境界線を黒でひく
        chart_line = alt.Chart(data[data['time'] == time]).transform_density(
            density=city,
            as_=[city, 'density'],
        ).mark_line(color='black', size = 0.4).encode(
            x=f"{city}:Q",
            y="density:Q",
            color = alt.value('black')
        )
        
        return chart_area + chart_line

    # 過去と現在のチャートを作成し、重ねる
    def create_combined_chart(data):
        chart_past = create_chart(data, 'past')
        chart_present = create_chart(data, 'present')
        # 色の凡例を追加
        return (chart_past + chart_present).encode(
            color=alt.Color('time:N', legend=alt.Legend(title="Time Period"))
        ).properties(title=city)

# 10個のチャートを作成
    charts.append(create_combined_chart(data))
    

# チャートを2行5列の形に並べる
row1 = alt.hconcat(*charts[:5])  # 最初の5つのチャートを水平に並べる
row2 = alt.hconcat(*charts[5:])  # 残りの5つのチャートを水平に並べる
final_chart = alt.vconcat(row1, row2)  # 2行のチャートを垂直に並べる

final_chart