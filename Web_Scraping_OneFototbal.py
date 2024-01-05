from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from itertools import zip_longest
import pandas as pd 
import numpy as np
from openpyxl import load_workbook
from datetime import datetime
#PARTIDOS DEL DIA DE HOY

# Configurar opciones del navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
#"--disable-gpu"

# Definir la ruta del controlador (chromedriver.exe)
path = "C:\\Users\\Usuario\\Documents\\Python\\WebScraping\\chromedriver-win64\\chromedriver.exe"

# Utilizar el servicio para proporcionar la ruta del ejecutable
service = Service(path)

# Crear la instancia del objeto webdriver.Chrome
driver = webdriver.Chrome(service=service, options=chrome_options)

# Abrir la página web
driver.get("https://onefootball.com/es/partidos")
time.sleep(10)  # Esperar 10 segundos para que la página cargue

# Esperar hasta 30 segundos para que el botón de aceptar cookies esté presente
wait = WebDriverWait(driver, 15)
cookie_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
cookie_button.click()

# Esperar 5 segundos después de aceptar las cookies
time.sleep(1)

# Desplazarse gradualmente por la página cada 5 segundos
for _ in range(7):  # Hacerlo 6 veces para recorrer toda la página
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    time.sleep(1)

# Esperar hasta 30 segundos para que al menos un elemento esté presente
wait = WebDriverWait(driver, 30)
elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="SimpleMatchCardTeam_simpleMatchCardTeam__name__7Ud8D"]')))
marcador = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="SimpleMatchCardTeam_simpleMatchCardTeam__score__UYMc_"]')))
imagenes = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//img[@class="ImageWithSets_of-image__img__pezo7 "]')))
jugando = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="SimpleMatchCard_simpleMatchCard__matchContent__prwTf"]')))

# ...

# Imprimir el texto de todos los elementos
Locales = []
Visitantes = []
marcador_local = []
marcador_visitante = []
imagen_local = []
imagen_visitante = []
estado = []

for index, img in enumerate(imagenes, start=1):
    img_url = img.get_attribute('src')
    if index % 2 == 1:  # Elementos impares (locales)
        imagen_local.append(img_url)
    else:  # Elementos pares (visitantes)
        imagen_visitante.append(img_url)

for index, i in enumerate(marcador, start=1):
    if index % 2 == 1:  # Elementos impares (locales)
        marcador_local.append(i.text)
    else:  # Elementos pares (visitantes)
        marcador_visitante.append(i.text)

for index, element in enumerate(elements, start=1):
    if index % 2 == 1:  # Elementos impares (locales)
        Locales.append(element.text)
    else:  # Elementos pares (visitantes)
        Visitantes.append(element.text)

if jugando:
    for index, i in enumerate(jugando):
        estado.append(i.text)
        
# Asegurarse de que la lista "estado" tenga la misma longitud que las demás listas
max_length = max(len(Locales), len(Visitantes), len(marcador_local), len(marcador_visitante), len(imagen_local), len(imagen_visitante))
estado += [0] * (max_length - len(estado))
fecha_actualizacion = datetime.now()

df = pd.DataFrame({"locales": Locales, "visitantes": Visitantes, "Marcador Local": marcador_local,
                   "Marcador Visitante": marcador_visitante, "Imagen Local": imagen_local, "Imagen Visitante": imagen_visitante,"Estado": estado})  # Tomar solo los primeros max_length elementos de la lista "estado"

df["Time"] = np.where((df["Marcador Local"] == '') & (df["Marcador Visitante"] == ''), 'Pendiente',
                      np.where(df["Estado"].str.contains("Fin"), 'Finalizado', 'Jugando'))

df['Fecha_Actualizacion'] = fecha_actualizacion

# Cerrar el navegador
driver.quit()

# Imprimir el DataFrame como tabla Markdown
#print(df.to_markdown(index=False))
# Guardar el DataFrame como archivo CSV
df.to_excel('partidos.xlsx', index=False)
print("Archivo 'partidos.csv' creado correctamente.")




#################################################################Inicia codigo de Clasificacion de la Premier--#############################################################

path = "C:\\Users\\Usuario\\Documents\\Python\\WebScraping\\chromedriver-win64\\chromedriver.exe"

# Utilizar el servicio para proporcionar la ruta del ejecutable
service = Service(path)

# Crear la instancia del objeto webdriver.Chrome
driver = webdriver.Chrome(service=service, options=chrome_options)

# Abrir la página web
driver.get("https://onefootball.com/es/competicion/premier-league-9/clasificacion")
time.sleep(10)  # Esperar 10 segundos para que la página cargue

# Esperar hasta 30 segundos para que el botón de aceptar cookies esté presente
wait = WebDriverWait(driver, 15)
cookie_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
cookie_button.click()

# Esperar 5 segundos después de aceptar las cookies
time.sleep(1)

# Desplazarse gradualmente por la página cada 5 segundos
for _ in range(3):  # Hacerlo 6 veces para recorrer toda la página
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    time.sleep(1)

# Esperar hasta 30 segundos para que al menos un elemento esté presente
wait = WebDriverWait(driver, 15)
Posicion = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Standing_standings__cell__5Kd0W"]')))
icono = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="Standing_standings__cell__5Kd0W Standing_standings__cellIcon__EbcOR"]')))
equipo = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="EntityLogo_entityLogo__29IUu Standing_standings__teamLogo__nnaR_"]')))
Nombre = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//p[@class="title-7-medium Standing_standings__teamName__psv61"]')))
PJ_DJ = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="Standing_standings__cell__5Kd0W Standing_standings__cellTextDimmed__vpZYH"]')))
G_D_P = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="Standing_standings__cell__5Kd0W Standing_standings__cellLargeScreen__ttPap Standing_standings__cellTextDimmed__vpZYH"]')))

Puestos = []
PTS = []
Nombre_Eqipo = []
PJ = []
DG = []
G = []
D = []
P = []
variable = []
Logo = []
Equipo_2 = []

for index, i in enumerate(Posicion, start=1):
    if index % 2 == 1:  # Elementos impares (locales)
        Puestos.append(i.text)
    else:  # Elementos pares (visitantes)
        PTS.append(i.text)
        
for index, i in enumerate(Nombre, start=1):
    Nombre_Eqipo.append(i.text)

for index, i in enumerate(PJ_DJ, start=1):
    if index % 2 == 1:  # Elementos impares (locales)
        PJ.append(i.text)
    else:  # Elementos pares (visitantes)
        DG.append(i.text)

for index, i in enumerate(G_D_P, start=1):
    variable.append(i.text)
    G = variable[0::3]
    D = variable[1::3]
    P = variable[2::3]
    
for index, imagen in enumerate(icono, start=1):
    img_url2 = imagen.get_attribute('src')
    Logo.append(img_url2)
    
for index, equi in enumerate(equipo, start=1):
    img_url_equipo = equi.get_attribute('src')
    Equipo_2.append(img_url_equipo)

driver.quit()

df2 = pd.DataFrame({"Puestos":Puestos,
                   "Nombre Eqipo":Nombre_Eqipo,
                   "PJ":PJ,
                   "G":G,
                   "D":D,
                   "P":P,
                   "DG":DG,
                   "PTS":PTS,
                   "Icono": Logo
                 })


# Cargar el archivo Excel existente
archivo_existente = "C:\\Users\\Usuario\\Documents\\Python\\WebScraping\\partidos.xlsx"
df_existente = pd.read_excel(archivo_existente)

# Tu DataFrame nuevo (df_nuevo)
# ...

# Nombre de la nueva hoja
nombre_nueva_hoja = 'nueva_hoja'

# Guardar el DataFrame nuevo en una nueva hoja
with pd.ExcelWriter(archivo_existente, engine='openpyxl', mode='a') as writer:
    df2.to_excel(writer, sheet_name=nombre_nueva_hoja, index=False)

print(f"Se ha agregado la información en una nueva hoja llamada '{nombre_nueva_hoja}' en el archivo existente.")

