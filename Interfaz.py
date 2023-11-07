import tkinter as tk
from tkinter import filedialog
import requests
from PIL import Image, ImageTk

# Reemplaza estos valores con tus propias credenciales de la API de Custom Vision
endpoint = 'TU_ENDPOINT'
subscription_key = 'TU_SUBSCRIPTION_KEY'
project_id = 'TU_PROYECTO_ID'
published_iteration_name = 'TU_ITERACION_PUBLICADA'

# Función para cargar una imagen y realizar la inferencia
def cargar_imagen():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as image_file:
            image_data = image_file.read()

        headers = {
            'Prediction-Key': subscription_key,
            'Content-Type': 'application/octet-stream'
        }

        params = {
            'iterationId': published_iteration_name
        }

        response = requests.post(endpoint + '/customvision/v3.0/Prediction/' + project_id + '/classify/iterations/' + published_iteration_name + '/image', headers=headers, params=params, data=image_data)

        if response.status_code == 200:
            result = response.json()
            mostrar_resultados(result)
        else:
            print('Error al hacer la predicción:', response.status_code)

# Función para mostrar los resultados en la interfaz
def mostrar_resultados(result):
    # Borra el resultado anterior si lo hay
    resultado_label.config(text='')

    # Analiza los resultados y muestra las etiquetas y probabilidades
    predictions = result['predictions']
    for prediction in predictions:
        tag = prediction['tagName']
        probability = prediction['probability']
        resultado_label.config(text=f'{tag}: {probability:.2%}')

# Crear la ventana de la aplicación
app = tk.Tk()
app.title('Reconocimiento de Imágenes con Custom Vision')

# Botón para cargar una imagen
cargar_imagen_button = tk.Button(app, text='Cargar Imagen', command=cargar_imagen)
cargar_imagen_button.pack()

# Etiqueta para mostrar los resultados
resultado_label = tk.Label(app, text='', wraplength=300)
resultado_label.pack()

app.mainloop()
