import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url = "https://www.mohfw.gov.in/"   # Url site to scrap data
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
text = soup.get_text()
rows = soup.find_all('tr')

for row in rows:
    row_td = row.find_all('td')
str_cells = str(row_td)           # change into string
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
df = pd.DataFrame(list_rows)
df = df[0].str.split(',', expand=True)
df.head(10)

#get Table Header
col_labels = soup.find_all('th')    # find header of table
all_header = []        
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
head = pd.DataFrame(all_header)   # Table Header
head = head[0].str.split(',', expand=True)

#concat Header and Data into one frame
frames = [head, df]
df = pd.concat(frames)     

# Clean the Data By removing string "[]"
df[0] = df[0].str.strip('[')  #Remove [ from data
df[4] = df[4].str.strip(']')  #Remove [ from data

df = df.rename(columns=df.iloc[0])       #rename column
df = df.dropna(axis=0, how='any')    # remove nan value
df = df.drop(df.index[0])   # remove Duplicate Index
print(df.head())

#uncomment me to download data into csv file format
#df.to_csv('Covid-19(India).csv','w')

