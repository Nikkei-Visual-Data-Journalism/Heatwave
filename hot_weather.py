import tabula
import requests
import pandas as pd
from bs4 import BeautifulSoup

tabula.environment_info()

##test
#pdf_path = 'https://www.fdma.go.jp/disaster/heatstroke/items/r5/heatstroke_sokuhouti_20230710.pdf'
#dfs = tabula.read_pdf(pdf_path, stream=True, pages=1)

#df = dfs[0]
#df_base = df.iloc[2:7, [0, 5]]

##Auto test

url = 'https://www.fdma.go.jp/disaster/heatstroke/post3.html'
r = requests.get(url)
text = r.text
soup = BeautifulSoup(text)

div_tag = soup.find_all('div', {'class': 'link-wrap mb30 txt'})

href_list = []
for i in div_tag[0].find_all('a', class_='link'):
  href_tag = i.get('href')
  href_list.append(href_tag)

href_list_app = []
for i in range(len(href_list)):
    test = list(href_list[i])
    test[:0] = 'https://www.fdma.go.jp/'
    test = ''.join(test)
    href_list_app.append(test)

href_list_app.reverse()

dfs = tabula.read_pdf(href_list_app[0], stream=True, pages=1)
df = dfs[0]
df_base = df.iloc[2:9, [0, 5]]

for pdf_path in href_list_app[1:]:
  dfs = tabula.read_pdf(pdf_path, stream=True, pages=1)
  df = dfs[0]
  df_add = df.iloc[2:9, [0, 5]]
  df_base = pd.concat([df_base, df_add], axis=0)

df_base = df_base.rename(columns={'Unnamed: 0': 'date', 'Unnamed: 4': '熱中症患者数'})

df_base['date'] = df_base['date'].str[:-1]
df_base

df_base.to_csv('hot_weahter.csv')