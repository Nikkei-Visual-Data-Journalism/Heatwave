#東京都の最高気温のヒートマップ（カバー用）を描画する
#元データは 'tokyo_max_temp.csv'（tokyo-maxtemp-1963-latest.pyで更新）
import pandas as pd
import altair as alt

#行数制限対応(デフォルトは5000)
alt.data_transformers.disable_max_rows()

#元データ
#東京の最高気温（1963-latest、随時更新）
filepath = './data-tokyo/tokyo_max_temp.csv'
tokyo = pd.read_csv(filepath, parse_dates=['date'])
#x軸用に年を揃える
tokyo['date_x'] = tokyo.date.apply(lambda x: x.replace(year=2000))


#altair用
source = tokyo

#カラースケール
domain_ = [0, 20, 25, 30, 35, 40]
range_ = ['#094575','#CCDD44', '#FFE600', '#FFB500','#C31923', '#6D0000']
scale_ = alt.Scale(domain=domain_, range=range_) 

#y軸のソート順（上が最新に）
sort_y = sorted(tokyo.year.unique(), reverse=True)

#X軸,Y軸に表示する日付（月初）
#カバー用ではX, Y軸は表示しないのでコメントアウト
#step_x = pd.date_range('2000-06-01','2000-09-01',freq='MS').to_list()
#step_y = list(range(1970,2030,10))


#描画
heatmap = alt.Chart(source).mark_rect(
    stroke='white', 
    strokeWidth=0.5
).encode(
    x=alt.X(
        'yearmonthdate(date_x):O', 
        #axis=alt.Axis(values = step_x, format='%-m/%-d'), 
        axis = None,
        title=''
    ),
    y=alt.Y(
        'year:O', 
        #axis=alt.Axis(values=step_y),
        axis = None,
        sort=sort_y,
        title=''
    ),
    color=alt.Color(
        'max:Q', 
        scale=scale_,
        #legend=alt.Legend(title='最高気温')
        legend = None
    )
).properties(width=600, height=200)

#出力
#heatmap.display()
heatmap.save('./img/tokyo_heatmap.png')