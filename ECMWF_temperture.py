#ECMWF
#https://charts.ecmwf.int/products/medium-z500-t850?base_time=202308141200&projection=opencharts_global&valid_time=202308141200

import ecmwf.data as ecdata
from magpye import GeoMap
from ecmwf.opendata import Client
import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
import matplotlib as mpl
import matplotlib.cm as cm


client = Client("ecmwf", beta=True)

parameters = ['gh', 't']
filename = './img/medium-z500-t850.grib'

#dateで0を基準にマイナスをセットすると過去データとれる。最新データ
client.retrieve(
    #date=0,
    #time=0,
    step=12,
    stream="oper",
    type="fc",
    levtype="pl",
    levelist=[500,850],
    param=parameters,
    target=filename
)

"""## Reading and processing the data
Now we can use **ecmwf.data** to read the file.
"""

data = ecdata.read(filename)

"""The **describe()** function will give us the overview of the dataset.  """

data.describe()

"""And an overview of one parameter"""

data.describe('gh')

"""We can use **ls()** function to list all the fields in the file we downloaded."""

data.ls()

"""The grib file contains all the parameters and levels, and we will use the **select()** function to filter what we need."""

t850 = data.select(shortName= 't',level=850)
t850.describe()

gh500 = data.select(shortName= 'gh',level=500)
gh500.describe()

"""Geopotential height has units gpm (geopotential meters), but on the ECMWF Open charts it is plotted in geopotential decameters. To reproduce the plot we need to divide by 10."""

gh500 /= 10

"""Temperature in our grib file is in Kelvin, but we would like to plot it in Celsius.  
We need to convert it before plotting.
"""

t850 -= 273.15

"""## Plotting the data
And finally, we can plot the data on the map.
"""
###新しいマッププロット###

grib_file = pygrib.open(filename)
grib_temperture = grib_file.select(name="Temperature") 

lats, lons = grib_temperture[0].latlons() 
mslp = grib_temperture[0].values

flat_lats= np.ravel(lats)
flat_lons= np.ravel(lons)

temperature_data = grib_file.select(name='Temperature')[1]
lats, lons = temperature_data.latlons()
temperature = temperature_data.values

#カラーマップを設定
#color_list = ['#E3E3E3', '#053061', '#2166ac', '#4393c3', '#EDED21', '#d6604d', '#b2182b', '#67001f']
color_list = ['#e3e3e3', '#8090ab','#4e6990','#094575','#215f91','#367aad','#4a97c9','#5FB4E6','#2bbdd0','#51c0a7','#6ebf91','#8ABD7D','#a4cf66','#CCDD44','#e4e22d','#FFE600','#ffcd00','#FFB500','#f79100','#ea6d10','#d9481c','#C31923','#6D0000','#d9481c','#F09192']

mycmap = mpl.colors.LinearSegmentedColormap.from_list('colormap_name', color_list)

#fig sizeを設定
plt.figure(figsize=(30, 16))


# 地図の範囲を設定
lon_min, lon_max = lons.min(), lons.max()
lat_min, lat_max = lats.min(), lats.max()

# 最小緯度がおかしかったので
m = Basemap(
    llcrnrlon=lon_min, llcrnrlat= -60,
    urcrnrlon=lon_max, urcrnrlat=70,
    projection='merc', resolution='l'
)

# マップの背景を描画
m.drawcoastlines()
#m.drawcountries()
#m.drawmapboundary()

# 温度データをカラーマップでプロットします
x, y = m(lons, lats)
temperature_celsius = temperature - 273.15  # ケルビンを摂氏に変換
contour = plt.contourf(x, y, temperature_celsius, cmap=mycmap, levels=25)

# カラーバー
divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="0.000001%", pad=0.0000000000000000000000000001)
#plt.colorbar(orientation='horizontal', cmap=mycmap, label='°C')

#追加
#ビジュアル周辺の余白を小さく
plt.subplots_adjust(top=0.001, bottom=0, left=0, right=0.001) 
plt.tight_layout()

#出力
plt.savefig('./img/ECMWF_temperture.png')

# グリッドを表示
#m.drawparallels(np.arange(lat_min, lat_max), fontsize=0.1)
#m.drawmeridians(np.arange(lon_min, lon_max, 10.), labels=[0, 0, 0, 1], fontsize=10)

#数値範囲
#cb.set_ticks(np.linspace(temperature_celsius.min(), 30, num=6))

#カラーバー単体で出力
#fig_colorbar = plt.figure(figsize=(3, 1))
#cb = plt.colorbar(contour, orientation='horizontal', label='°C', cmap=mycmap)
#cb.ax.tick_params(labelsize=10)

# カラーバー用の図を作成し、カラーバーをプロット
fig_colorbar = plt.figure(figsize=(5, 1))
cb = plt.colorbar(contour, orientation='horizontal', label='°C', cax=fig_colorbar.add_axes([0.1, 0.1, 0.8, 0.8]), cmap=mycmap)
cb.ax.tick_params(labelsize=10)


fig_colorbar.savefig('./img/colorbar_figure.png')





#GeoMap()の()内で投影地域を変える。
#fig = GeoMap()

#fig.coastlines(land_colour="cream",resolution="medium")


#fig.contour_shaded(t850, style="temperature_rainbow_3")

#等高線
#fig.contour_lines(gh500, style="black_i4")

#fig.coastlines(resolution="medium")
#fig.gridlines()

#タイトル、凡例
#fig.title(["<grib_info key='valid-date' format='%Y-%m-%d' where='shortName=t'/>　"])
#fig.legend()
#fig.footer()

#出力
##img dirに変更
#fig.save('./img/ECMWF_temperture.png')

#追加作業候補
##titleに入れている'valid-date'を'%Y年%-m月%-d日'形式のテキストにして別のファイルに入れてgithub上におくように変更
##github上のテキスト-->htmlタグで呼び出してRCB上に置き、動的にテキスト表示できる


"""Note that plot produced using open data dataset will slightly differ from one from Open Charts. This is due to different resolution of the data.  
Open data is on 0.4x0.4 resolution, while high resolution data is 0.1x0.1 grid.
"""

