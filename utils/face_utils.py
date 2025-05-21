import os
import cv2
import face_recognition
import tkinter as tk    


# ================= REGISTRO DE ROSTRO  =================
def registrar_foto(nombre_usuario):
    while True:
        camara = cv2.VideoCapture(0)
        print("📸 Presiona 's' para tomar la foto...")

        window_name = "Captura de rostro (Presiona 's' para tomar la foto)"
        ancho, alto = 640, 480

        # Captura un frame inicial para crear la ventana
        ret, frame = camara.read()
        if not ret:
            print("❌ Error al acceder a la cámara.")
            camara.release()
            cv2.destroyAllWindows()
            return

        # Mostrar el primer frame para que la ventana exista
        cv2.imshow(window_name, frame)

        # Centrar la ventana después de mostrar el primer frame
        centrar_ventana_cv2(window_name, ancho, alto)

        foto_tomada = False
        ruta_guardado = None

        while True:
            ret, frame = camara.read()
            if not ret:
                print("❌ Error con la cámara.")
                break

            cv2.imshow(window_name, frame)

            key = cv2.waitKey(100) & 0xFF
            if key == ord('s'):
                os.makedirs(os.path.join("assets", "rostros"), exist_ok=True)
                ruta_guardado = os.path.join("assets", "rostros", f"{nombre_usuario}.jpg")
                cv2.imwrite(ruta_guardado, frame)
                print(f"✅ Rostro guardado: {ruta_guardado}")
                foto_tomada = True
                break

        camara.release()
        cv2.destroyAllWindows()

        if foto_tomada and ruta_guardado:
            # Verificar si el rostro es válido
            try:
                imagen = face_recognition.load_image_file(ruta_guardado)
                encoding = face_recognition.face_encodings(imagen)[0]
                print("✅ Rostro válido.")
                break  # Sale del bucle principal si el rostro es válido
            except IndexError:
                print("⚠️ No se detectó rostro, repite el registro.")
                os.remove(ruta_guardado)
                # Espera un momento antes de volver a abrir la cámara
                cv2.waitKey(1000)
        else:
            break

# ============ PARTE 1: RECONOCIMIENTO FACIAL ============
def reconocer_rostro():
    rostros_conocidos = []
    nombres = []

    # Cargar los rostros conocidos
    for archivo in os.listdir("assets/rostros"):
        ruta = os.path.join("assets", "rostros", archivo)
        imagen = face_recognition.load_image_file(ruta)
        codificaciones = face_recognition.face_encodings(imagen)
        if codificaciones:  # Verifica que haya rostro en la imagen
            rostros_conocidos.append(codificaciones[0])
            nombres.append(os.path.splitext(archivo)[0])

    video = cv2.VideoCapture(0)
    print("📸 Buscando rostro... (presiona 'q' para salir manualmente)")

    window_name = "Reconocimiento Facial (presiona 'q' para salir manualmente)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # Elimina o comenta la siguiente línea si no quieres ventana siempre en primer plano
    # cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    TOLERANCIA = 0.3

    while True:
        ret, frame = video.read()
        if not ret:
            print("⚠️ No se pudo capturar imagen de la cámara.")
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ubicaciones = face_recognition.face_locations(rgb)
        codificaciones = face_recognition.face_encodings(rgb, ubicaciones)

        for (top, right, bottom, left), cod in zip(ubicaciones, codificaciones):
            distancias = face_recognition.face_distance(rostros_conocidos, cod)

            if len(distancias) > 0:
                menor_distancia = min(distancias)
                indice_mejor = distancias.tolist().index(menor_distancia)

                if menor_distancia < TOLERANCIA:
                    nombre = nombres[indice_mejor]
                    print(f"✅ Rostro reconocido: {nombre} (Distancia: {menor_distancia:.2f})")
                    video.release()
                    cv2.destroyAllWindows()
                    return nombre
                else:
                    nombre = "Desconocido"
            else:
                nombre = "Desconocido"

            # Dibujar rectángulo
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, nombre, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Mostrar el video
        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("❌ No se reconoció ningún rostro.")
    video.release()
    cv2.destroyAllWindows()
    return None



#============ FUNCIONES AUXILIARES ============

def centrar_ventana(ventana, ancho=300, alto=200):
    ventana.update_idletasks()  # Asegura que se obtengan dimensiones correctas

    # Obtiene el tamaño de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Calcula coordenadas x e y
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)

    # Define tamaño y posición
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def centrar_ventana_cv2(nombre_ventana, ancho=640, alto=480):
    # Obtener resolución de pantalla usando Tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana de Tkinter
    pantalla_ancho = root.winfo_screenwidth()
    pantalla_alto = root.winfo_screenheight()
    root.destroy()

    # Calcular coordenadas para centrar
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2

    # Ajustar tamaño y posición de la ventana OpenCV
    cv2.namedWindow(nombre_ventana, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(nombre_ventana, ancho, alto)
    cv2.moveWindow(nombre_ventana, x, y)
