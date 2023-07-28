# Heatwave
猛暑ビジュアライゼーション

|data|source|codes|output|update_frequency|workflow|visualization|note|
| ---- | ---- | ---- | ---- | ---- |---- | ---- |---- |
|現在の気温（日本）|[アメダス](https://www.jma.go.jp/bosai/map.html#5/34.488/137.021/&elem=temp&contents=amedas&interval=60)|[amedas_latest_data.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/amedas_latest_data.py)|amedas_latest_all.csv<br>amedas_latest_temp.csv|1時間おき(10分程度遅れ)|毎時10, 40分|Flourish|[参考](https://okumuralab.org/~okumura/python/amedas.html)|
|世界の平均気温|[ClimeteReanalyzer/Daily 2-meter Air Temperature](https://climatereanalyzer.org/clim/t2_daily/)|[world_temperature.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/world_temperature.py)|[world_temperature.csv](ここにURLを貼る)|毎日(UTC 5:00AM)|毎日(UTC 5:05)|[Flourish](https://app.flourish.studio/visualisation/14531196/edit)|@hiroki-sakuragi|



▼02summerday_point_num_github.py（有年）  
日本　　📈今年の真夏日猛暑日観測地点数のグラフ用コード

▼04_japan_temperature_github.py（有年）  
📈主要都市（東京）の真夏日・猛暑日の日数（6月1日〜前日の範囲）、時系列比較コード  
コード内で結合に使う過去データは'1963_2022_all_202306only.csv'   
　＊10月に入るとデータ欠損でエラーになる  
 
▼04_japan_temperature_github.py（有年）  
📈東京の日別最高気温ヒートマップ用コード（1963〜2022年の6月1日〜9月31日と2023年の6月1日〜前日まで）    
　＊10月に入るとデータ欠損でエラーになる  



▼hot_weather.py(田中)
救急搬送者数のデータ入手コード

▼ECMWF_temperture.py(田中）
世界地図気温

▼hot_index.py
環境省の暑さ指数、flourishは連携できておらず（0727）



