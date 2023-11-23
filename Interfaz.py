import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
from io import BytesIO

class CustomVisionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Custom Vision App')
        self.setGeometry(100, 100, 800, 600)

        # Etiqueta para mostrar la imagen
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 400)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap('placeholder.jpg'))

        # Botón para cargar una imagen
        load_button = QPushButton('Cargar Imagen', self)
        load_button.clicked.connect(self.loadImage)

        # Etiqueta para mostrar los resultados de la predicción
        self.result_label = QLabel('Resultados de Predicción', self)
        self.result_label.setAlignment(Qt.AlignCenter)

        # Diseño de la interfaz con QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(load_button)
        layout.addWidget(self.result_label)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def loadImage(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Cargar Imagen', '', 'Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)', options=options)

        if file_path:
            # Mostrar la imagen
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)

            # Realizar la predicción
            self.predictImage(file_path)

    def predictImage(self, file_path):
        try:
            # Leer la imagen como datos binarios
            with open(file_path, 'rb') as image_file:
                image_data = image_file.read()

            # Reemplaza con tus propias credenciales de Custom Vision
            endpoint = 'https://perrosygatos-prediction.cognitiveservices.azure.com'
            prediction_key = 'b6efc9d10e15470dbd1c9c733fa01adf'
            project_id = '2a1db91e-9e9d-4a9c-a625-30169909b6a8'
            iteration_id = 'Iteration1'  # Reemplaza con el ID correcto

            params = {'iterationId': iteration_id}

            # Configurar los encabezados de la solicitud
            headers = {
                'Prediction-Key': prediction_key,
                'Content-Type': 'application/octet-stream'
            }

            # Realizar la solicitud HTTP
            response = requests.post(f'{endpoint}/customvision/v3.0/Prediction/{project_id}/classify/iterations/{iteration_id}/image', headers=headers, params=params, data=image_data)

            if response.status_code == 200:
                result = response.json()
                predictions = result.get('predictions', [])
                if predictions:
                    # Mostrar la etiqueta y probabilidad de la predicción principal
                    main_prediction = predictions[0]
                    tag = main_prediction['tagName']
                    probability = main_prediction['probability']
                    self.result_label.setText(f'Predicción: {tag} ({probability:.2%})')
                else:
                    self.result_label.setText('No se encontraron predicciones.')
            else:
                print('Error al hacer la predicción:', response.status_code)

        except Exception as e:
            print(f'Error al procesar la imagen: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CustomVisionApp()
    mainWindow.show()
    sys.exit(app.exec_())

