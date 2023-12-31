from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd 

#PARTIDOS DEL DIA DE HOY

# Configurar opciones del navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")

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
for _ in range(6):  # Hacerlo 6 veces para recorrer toda la página
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    time.sleep(1)

# Esperar hasta 30 segundos para que al menos un elemento esté presente
wait = WebDriverWait(driver, 30)
elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="SimpleMatchCardTeam_simpleMatchCardTeam__name__7Ud8D"]')))
marcador = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="SimpleMatchCardTeam_simpleMatchCardTeam__score__UYMc_"]')))
imagenes = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//img[@class="ImageWithSets_of-image__img__pezo7 "]')))

# Imprimir el texto de todos los elementos
Locales = []
Visitantes = []
marcador_local = []
marcador_visitante = []
imagen_local = []
imagen_visitante = []

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

df = pd.DataFrame({"locales": Locales, "visitantes": Visitantes, "Marcado Local": marcador_local, "Marcador Visitante": marcador_visitante, "Imagen Local": imagen_local, "Imagen Visitante": imagen_visitante})

# Cerrar el navegador
driver.quit()

# Imprimir el DataFrame como tabla Markdown
print(df.to_markdown(index=False))

# Guardar el DataFrame como archivo CSV
df.to_csv('partidos.csv', index=False)
print("Archivo 'partidos.csv' creado correctamente.")


#PARTIDOS DE LA PREMIER 