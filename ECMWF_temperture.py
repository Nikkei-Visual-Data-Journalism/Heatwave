import ecmwf.data as ecdata
from magpye import GeoMap
from ecmwf.opendata import Client

client = Client("ecmwf", beta=True)

parameters = ['gh', 't']
filename = 'medium-z500-t850.grib'
filename


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

#GeoMap()の()内で投影地域を変える。
fig = GeoMap()

fig.coastlines(land_colour="cream",resolution="medium")


fig.contour_shaded(t850, style="temperature_rainbow_3")

#等高線
#fig.contour_lines(gh500, style="black_i4")

fig.coastlines(resolution="medium")
#fig.gridlines()

#fig.title(["<grib_info key='valid-date' format='%Y-%m-%d' where='shortName=t'/>　"])
fig.legend()
fig.footer()

fig.save('ECMWF_temperture.png')

"""Note that plot produced using open data dataset will slightly differ from one from Open Charts. This is due to different resolution of the data.  
Open data is on 0.4x0.4 resolution, while high resolution data is 0.1x0.1 grid.
"""

