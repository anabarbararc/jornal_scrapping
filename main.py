import requests
from bs4 import BeautifulSoup as bs
import dateparser
import pandas as pd



# Cod for o Liberal 


 
response = requests.get('https://liberal.com.br/?s=Sindicato+Trabalhadores+Campinas')
soup=bs(response.text,'html.parser')
articles = soup.find('div', {"class": "results-content box-article"})

#cria lista com as urls retornadas da pesquisa do site X
urls=[i.get('href') for i in articles.find_all('a') ]


# cria um Dataframe com a lista de sites 
df=pd.DataFrame(columns=['url','data','Contem'])
keywords=['sindicato', 'campinas', 'stmc'] #keyword para tentar fitra a primeira frases
for i in urls[:-1]:
    page=requests.get(i)
    if page.ok:  # o jornal tem ums link quebrados isso serve para filtrar
        timer=bs(page.text).find('p',{'class':'data'})
        data=dateparser.parse(timer.text.split('às')[0][6:], languages=['pt'])
        cotem=set(keywords) & set(page.text.split())
        df.loc[i]=[i,data,cotem]

df.to_csv(r'C:\Users\jaime\OneDrive\Documentos\Patota\jornal_scrapping\Oliberal.csv')