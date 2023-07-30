import pandas as pd
#最新データ
url = "./data-maxtemp/daily-data/jma-maxtemp-latest.csv"
data = pd.read_csv(url)

#最高気温のランキングデータを作成
rank_df= data.copy()
rename_dic = {col:'maxtemp' for col in data.columns if '最高気温(℃)' in col}
rename_dic.update({col: 'maxtemp_h' for col in rank_df.columns if '今日の最高気温起時（時' in col})
rename_dic.update({col:'maxtemp_t' for col in rank_df.columns if '今日の最高気温起時（分' in col})
rename_dic.update({col:'平年気温との差' for col in rank_df.columns if '平年差' in col})
rename_dic.update({col:'max_value' for col in rank_df.columns if '観測史上1位の値（℃）' in col})

#カラムの日本語整える
rank_df = rank_df.rename(columns=rename_dic)
rank_df = rank_df.dropna(subset=['maxtemp_h','maxtemp_t'])
rank_df['最高気温の時刻'] = rank_df.maxtemp_h.astype(int).astype(str)+ ':'+ rank_df.maxtemp_t.astype(int).astype(str)
rank_df['最高気温の時刻'] = pd.to_datetime(rank_df['最高気温の時刻'],format='%H:%M').dt.strftime('%H:%M')
#必要な情報を整形
###観測地点の一覧
url = 'https://raw.githubusercontent.com/Nikkei-Visual-Data-Journalism/Heatwave/main/data-maxtemp/meta/points_list.csv'
points = pd.read_csv(url)
#地名と記録
rank_df['地名'] = rank_df['観測所番号'].map(points.set_index('観測所番号').name.to_dict())
rank_df['都道府県名'] = rank_df['観測所番号'].map(points.set_index('観測所番号').pref.to_dict())
rank_df['記録'] = rank_df['今年最高'].replace(1,'今年最高')

rank_df.loc[rank_df.maxtemp > rank_df.max_value, '記録'] = '観測史上最高'

#
rank_df = rank_df.rename(columns={'maxtemp':'最高気温'})
rank_df = rank_df[['観測所番号','都道府県名','地名','最高気温','平年気温との差','記録']].sort_values(by='最高気温', ascending=False)

#Flourishのフィルター表示用
rank_df['項目'] = rank_df['都道府県名'].copy()
#上位10
top10 = rank_df.head(10).copy()
top10['項目'] = '全国の上位10'
#観測史上最高
record_high = rank_df[rank_df['記録'] == '観測史上最高'].copy()
record_high['項目'] = '観測史上最高を更新'
#今年最高
year_high = rank_df[rank_df['記録'] == '今年最高'].copy()
year_high['項目'] = '今年最高を更新'

rank_df = pd.concat([top10, record_high, year_high, rank_df])
rank_df.to_csv('./data/maxtemp-ranking-latest.csv',index=False)