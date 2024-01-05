from PIL import Image
import requests

print("Ingresa la imagen a descargar")
url = str(input())
name = "imagen.jpg"
size = (200, 200)

# Utiliza "Image" en lugar de "image" en la siguiente línea
imagen = Image.open(requests.get(url, stream=True).raw)

# Corrige el nombre de la variable y el método de redimensionamiento
img = imagen.resize(size)

# Crea el directorio "images" si no existe
import os
os.makedirs("images", exist_ok=True)

# Guarda la imagen redimensionada en el directorio "images"
img.save('images/' + name)
input("Imagen descargada. Presiona Enter para salir.")