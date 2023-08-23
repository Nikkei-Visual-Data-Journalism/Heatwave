# Heatwave
猛暑ビジュアライゼーション
## 日本
|data|source|code|バックデータ|更新頻度<br>source_data|更新頻度<br>workflow|visualization|note|
| ---- | ---- | ---- | ---- | ---- |---- | ---- |---- |
|現在の気温|[アメダス](https://www.jma.go.jp/bosai/map.html#5/34.488/137.021/&elem=temp&contents=amedas&interval=60)|[amedas_latest_data.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/amedas_latest_data.py)|[amedas_latest_temp.csv]()|1時間おき(10分程度遅れ)|毎時10, 40分|[Flourish](https://app.flourish.studio/visualisation/14574559/edit)|[参考](https://okumuralab.org/~okumura/python/amedas.html)|
|暑さ指数（実況値）|[環境省](https://www.wbgt.env.go.jp/wbgt_data.php)|GASで取得|[GoogleSheet](https://docs.google.com/spreadsheets/d/1FtM00wuPyewYqz6MGqOQDJOplV4G2eWsEXLkgZtzYfM/edit#gid=95543419)|1時間おき（30分頃）|1時間おき(30分頃)|[Flourish](https://app.flourish.studio/visualisation/14816595/edit)|[経緯はこちら](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/issues/1#issue-1842373649)|
|今年の真夏日猛暑日観測地点数|[気象庁](https://www.data.jma.go.jp/obd/stats/etrn/view/summer.php?)|[02summerday_point_num_github.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/02summerday_point_num_github.py)|[japan_heatpoint_count.csv](https://raw.githubusercontent.com/Nikkei-Visual-Data-Journalism/Heatwave/main/data/japan_heatpoint_count.csv)|毎日(UTC 1:00AM)|3時間おき|Flourish<br>[全国の猛暑日と真夏日の日数](https://public.flourish.studio/visualisation/14540327/)|@YukikoUne|
|東京の最高気温ヒートマップ（1963~）|[気象庁](https://www.data.jma.go.jp/risk/obsdl/index.php)<br>[1963_2022_all_202306only.csv](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/1963_2022_all_202306only.csv)<br>[2023年7月~](https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=7)|[04_tokyo_temperature_heatmap.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/04_tokyo_temperature_heatmap.py)|[tokyo_max_temp.csv](https://raw.githubusercontent.com/Nikkei-Visual-Data-Journalism/Heatwave/main/data/tokyo_max_temp.csv)|毎日(UTC 1:00AM)|3時間おき|Flourish<br>[東京の夏の最高気温ヒートマップ](https://public.flourish.studio/visualisation/14545930/)|@YukikoUne<br>10月に入るとデータ欠損でエラーになる|
|東京の猛暑日の数（1963~）|[気象庁](https://www.data.jma.go.jp/risk/obsdl/index.php)<br>[tokyo_maxtemp_byD_until202306.csv](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/tokyo_maxtemp_byD_until202306.csv)<br>[2023年7月~](https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2023&month=7)|[06_tokyo_max_temperature_annual.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/06_tokyo_max_temperature_annual.py)|[tokyo_maxtemp_data_until_now.csv](https://raw.githubusercontent.com/Nikkei-Visual-Data-Journalism/Heatwave/main/data/tokyo_maxtemp_data_until_now.csv)|毎日(UTC 1:00AM)|1時間おき)|Flourish<br>[02東京の猛暑日の日数](https://public.flourish.studio/visualisation/14572935/)|@YukikoUne|

## 世界
|data|source|codes|output|更新頻度<br>source_data|更新頻度<br>workflow|visualization|note|
| ---- | ---- | ---- | ---- | ---- |---- | ---- |---- |
|世界の平均気温|[ClimeteReanalyzer/Daily 2-meter Air Temperature](https://climatereanalyzer.org/clim/t2_daily/)|[world_temperature.py](https://github.com/Nikkei-Visual-Data-Journalism/Heatwave/blob/main/world_temperature.py)|[world_temperature.csv](ここにURLを貼る)|毎日(UTC 5:00AM)|毎日1回(UTC 5:05)|Flourish<br>[世界の平均気温](https://public.flourish.studio/visualisation/14531196/)|@hiroki-sakuragi|
|世界の上空気温（地図）|[ECMWF](https://charts.ecmwf.int/products/medium-z500-t850)|ECMWF_temperture.py|ECMWF_temperature.png|毎日2回(UTC 6:00, 18:00前後)|毎日2回(UTC 7:00, 19:00)|visualization|UTC 0:00, 12:00にHRESモデルの実行開始→およそ6時間後に反映|

  

▼hot_weather.py(田中)
救急搬送者数のデータ入手コード

▼city_temperature_visualize.py
ftのdensity chartを模倣。元データは"2m_temp_1950to1954.csv"と”2m_temp_2019to2023.csv”。データ取得はコードは'data_cdsAPI_1950to1954'と'data_cdsAPI_2019to2023'。データ元はhttps://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=form

