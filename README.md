# Heatwave
猛暑ビジュアライゼーション

|data|source|codes|output|update_frequency|workflow|visualization|note|
| ---- | ---- | ---- | ---- | ---- |---- | ---- |---- |
|現在の気温（日本）|[アメダス](https://www.jma.go.jp/bosai/map.html#5/34.488/137.021/&elem=temp&contents=amedas&interval=60)|[amedas_latest_data.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/amedas_latest_data.py)|amedas_latest_all.csv<br>amedas_latest_temp.csv|1時間おき(10分程度遅れ)|毎時10, 40分|Flourish|[参考](https://okumuralab.org/~okumura/python/amedas.html)|
|世界の平均気温|[ClimeteReanalyzer/Daily 2-meter Air Temperature](https://climatereanalyzer.org/clim/t2_daily/)|[world_temperature.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/world_temperature.py)|[world_temperature.csv](ここにURLを貼る)|毎日(UTC 5:00AM)|毎日(UTC 5:05)|[Flourish](FlourishのpublicのURLを入れる)|@hiroki-sakuragi|
|今年の真夏日猛暑日観測地点数|[気象庁](https://www.data.jma.go.jp/obd/stats/etrn/view/summer.php?)|[02summerday_point_num_github.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/02summerday_point_num_github.py)|[japan_heatpoint_count.csv](ここにURLを貼る)|毎日(UTC 5:00AM)|毎日(UTC 5:05)|[Flourish](FlourishのpublicのURLを入れる)|@YukikoUne|
|東京の最高気温ヒートマップ（1963~）|[気象庁](https://www.data.jma.go.jp/risk/obsdl/index.php)<br>[1963_2022_all_202306only.csv](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/1963_2022_all_202306only.csv)<br>[2023年7月~](https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=7)|[04_tokyo_temperature_heatmap.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/04_tokyo_temperature_heatmap.py)|[tokyo_max_temp.csv](ここにURLを貼る)|毎日(UTC 5:00AM)|毎日(UTC 5:05)|[Flourish](FlourishのpublicのURLを入れる)|@YukikoUne<br>10月に入るとデータ欠損でエラーになる|
|東京の猛暑日の数（1963~）|[気象庁](https://www.data.jma.go.jp/risk/obsdl/index.php)<br>[tokyo_maxtemp_byD_until202306.csv](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/tokyo_maxtemp_byD_until202306.csv)<br>[2023年7月~](https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=7)|[06_tokyo_max_temperature_annual.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/06_tokyo_max_temperature_annual.py)|[tokyo_maxtemp_data_until_now.csv](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/tokyo_maxtemp_data_until_now.csv)|毎日(UTC 5:00AM)|毎日(UTC 5:05)|[Flourish](FlourishのpublicのURLを入れる)|@YukikoUne|

  

▼hot_weather.py(田中)
救急搬送者数のデータ入手コード

▼ECMWF_temperture.py(田中）
世界地図気温

▼hot_index.py
環境省の暑さ指数、flourishは連携できておらず（0727）



