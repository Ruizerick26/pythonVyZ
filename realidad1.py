import cv2
import numpy as np
import cv2.aruco as aruco
import requests

# Reemplaza con tu token y pines virtuales
token = "nPIa6kinb2ceXh-EAmgwoLIabhql02p1"

# Crear un diccionario de URLs de la API Blynk para obtener valores
urls_blynk_api = {
    0: {
        "valor": f'https://blynk.cloud/external/api/get?token={token}&V5',
        "tipo": "humedad"
    },
    1: {
        "valor": f'https://blynk.cloud/external/api/get?token={token}&V7',
        "tipo": "temperatura"
    },
    2: {
        "valor": f'https://blynk.cloud/external/api/get?token={token}&V3',
        "tipo": "luz"
    }
    # Puedes agregar más configuraciones para otros IDs si es necesario
}

# Crear un objeto detector de marcadores
parametros = cv2.aruco.DetectorParameters()

# Crear un diccionario de marcadores ArUco
aruco_diccionario = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)

# Inicializar la cámara (asegúrate de tener una cámara conectada)
captura = cv2.VideoCapture(0)

# Cargar la imagen que deseas superponer
nueva_imagen = cv2.imread("C:/Users/Erick/Desktop/trabajos U/CUARTO SEMESTRE\Desarrollo de IOT/aruco/temhum.jpg")  # Reemplaza con la ruta de tu imagen

while True:
    # Capturar un fotograma o cuadro (frame) de la cámara
    lectura, frame = captura.read()

    # Convertir el fotograma a escala de grises
    cuadro_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Crear un objeto de detector ArUco
    detector = aruco.ArucoDetector(aruco_diccionario, parametros)

    # Detectar marcadores ArUco
    esquinas, identificador, puntosRechazados = detector.detectMarkers(cuadro_gris)

    # Inicializar valores de humedad, temperatura y luz
    valores = {}

    if identificador is not None:
        # Solo obtén valores si hay al menos un marcador detectado
        for i in range(len(identificador)):
            id_marcador = identificador[i][0]
            valores[id_marcador] = {
                "valor": requests.get(urls_blynk_api[id_marcador]["valor"]).text,
                "tipo": urls_blynk_api[id_marcador]["tipo"]
            }

        # Dibujar los marcadores detectados
        aruco.drawDetectedMarkers(frame, esquinas, identificador)

        for i in range(len(identificador)):
            # Obtener el ID del marcador actual
            id_marcador = identificador[i][0]

            # Obtener las esquinas del marcador actual
            marker_corners = esquinas[i][0]

            # Definir la posición y el tamaño de la superposición
            x, y, w, h = cv2.boundingRect(marker_corners)

            # Escalar la imagen superpuesta para que se ajuste al tamaño del marcador
            imagen_sobrepuesta = cv2.resize(nueva_imagen, (w, h))

            # Superponer la imagen en el marco
            frame[y:y+h, x:x+w] = imagen_sobrepuesta

            # Superponer el texto (Humedad, Temperatura o Luz)
            valor = valores[id_marcador]["valor"]
            tipo = valores[id_marcador]["tipo"]

            texto = f"ID {id_marcador}: {tipo} {valor}"
            cv2.putText(frame, texto, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Mostrar el resultado en una ventana
    cv2.imshow('Aruco', frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar la ventana
captura.release()
cv2.destroyAllWindows()