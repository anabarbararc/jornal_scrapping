import requests
from bs4 import BeautifulSoup as bs
import dateparser

response = requests.get('https://liberal.com.br/?s=Sindicato+Trabalhadores+Campinas')

data = response.text

soup = bs(response.text, 'html.parser')

articles = soup.find('div', {"class": "results-content box-article"})

#print(articles.a)
#for x in articles.find_all('a'):
#    print(x.get('href'))

url2 = articles.find_all('a')[0].get('href')
site2 = requests.get(url2)
data_article = site2.text

data_time = bs(data_article).find('p',{"class":"data"})

date = data_time.text.split('às')[0][6:]

print(dateparser.parse(date, languages=['pt']) )

print(set(['sindicato', 'campinas', 'stmc']) & set(data_article.lower().split()) )
