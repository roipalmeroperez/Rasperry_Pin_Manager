import cv2, time

def takeFoto(route, name):
	# 1. Inicializar la cámara (0 suele ser la webcam USB por defecto)
    cap = cv2.VideoCapture(0)
    
    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    print("Cámara detectada. Estabilizando exposición...")
    # 2. Dejar que la cámara se adapte a la luz ambiental (2 segundos)
    time.sleep(2)

    # 3. Leer un fotograma (frame) de la cámara
    ret, frame = cap.read()

    # Si la lectura fue exitosa, guardamos la imagen
    if ret:
        # 4. Guardar la imagen en el disco
        cv2.imwrite(route + name, frame)
        print("¡Foto guardada con éxito como '{nombre_archivo}'!")
    else:
        print("Error: No se pudo capturar el fotograma.")

    # 5. Liberar la cámara para que otros programas puedan usarla
    cap.release()

if __name__ == '__main__':
	takeFoto('./', 'foto.jpg')
