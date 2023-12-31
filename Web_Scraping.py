import requests #mercadolibre devuelve html
import time
from selenium import webdriver
from bs4 import BeautifulSoup #Sirve para hacer el scraping
from lxml import etree
import pandas as pd

r = requests.get('https://listado.mercadolibre.com.co/computadores')
r.status_code
r.content
soup = BeautifulSoup(r.content,'html.parser')
titulos = soup.find_all('h2',attrs = {"class":"ui-search-item__title"})
titulos = [i.text for i in titulos]
print(titulos)
print(len(titulos))
url = soup.find_all('a',attrs={"ui-search-item__group__element ui-search-link__title-card ui-search-link"})
url = [i.get('href') for i in url] #posibles opciones de etiquetado
cantidad_elementos = len(url)
lista_texto = []

for elemento in url:
    elemento_texto = str(elemento)
    lista_texto.append(elemento_texto)
    
#print(cantidad_elementos)
#print(url)


url = soup.find_all('a',attrs={"class":"andes-money-amount__fraction"})
dom = etree.HTML(str(soup))
precios = dom.xpath('//li[@class="ui-search-layout__item"]//div[@class="ui-search-result__content-columns"]/div[@class="ui-search-result__content-column ui-search-result__content-column--left"]/div[1]/div//div[@class="ui-search-price__second-line"]//span[@class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]/span[2]')
len(precios)
precios = [i.text for i in precios]
#print(precios)

pd.set_option('display.max_colwidth', None)

# Crear el DataFrame
df = pd.DataFrame({"Titulo": titulos, "Precios": precios, "Links": lista_texto})

# Imprimir el DataFrame como tabla Markdown
print(df.to_markdown(index=False))

# Guardar el DataFrame como archivo CSV
df.to_csv('Computadores_MercadoLibre.csv', index=False)
print("Archivo 'Computadores_MercadoLibre.csv' creado correctamente.")