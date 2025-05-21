from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox

#==============Grabar la voz========================
def grabar_voz(nombre_archivo="voz_actual.wav", duracion=4, fs=16000):
    # Mostrar mensaje de confirmación
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    root.destroy()  # Cierra la ventana oculta

    print("🔴 Grabando voz...")
    audio = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write(nombre_archivo, fs, audio)
    print(f"✅ Grabación guardada en {nombre_archivo}")



#============Registro de voz========================
def registrar_voz(nombre_usuario, root):

    messagebox.showinfo("Comenzar grabación", "Presiona Aceptar y comienza a hablar.")

    # Mostrar ventana "Escuchando audio..." que se cierra sola
    popup = tk.Toplevel(root)
    popup.title("Grabando voz")
    popup.geometry("300x100")
    label = tk.Label(popup, text="🎙️ Escuchando audio...", font=("Arial", 12))
    label.pack(expand=True)

    # Forzar renderizado antes de grabar
    popup.update()

    # Grabar audio (bloquea 4 segundos)
    grabar_voz("voz_actual.wav", duracion=4)

    # Cerrar automáticamente después de grabar
    popup.destroy()

    # Procesar la voz y guardar
    print("🔊 Procesando voz...")
    wav = preprocess_wav("voz_actual.wav")
    encoder = VoiceEncoder()
    emb = encoder.embed_utterance(wav)

    os.makedirs("assets/voces", exist_ok=True)
    np.save(os.path.join("assets", "voces", f"{nombre_usuario}.npy"), emb)
    os.remove("voz_actual.wav")
    print(f"✅ Voz guardada: assets/voces/{nombre_usuario}.npy")


#============Reconocimiento de voz========================
def reconocer_voz(nombre_usuario):
    ruta_voz = os.path.join("assets", "voces", f"{nombre_usuario}.npy")
    if not os.path.exists(ruta_voz):
        print("❌ No hay registro de voz para este usuario.")
        return False

    emb_guardado = np.load(ruta_voz)
    encoder = VoiceEncoder()
    umbral = 0.75
    intentos_maximos = 3

    for intento in range(intentos_maximos):

        messagebox.showinfo("Dí tu contraseña de audio", f"Intento {intento+1} de {intentos_maximos}.\nPresiona Aceptar y comienza a hablar.")
        grabar_voz( "voz_actual.wav", duracion=4)

        wav_actual = preprocess_wav("voz_actual.wav")
        emb_actual = encoder.embed_utterance(wav_actual)

        os.remove("voz_actual.wav")

        similitud = np.dot(emb_guardado, emb_actual) / (np.linalg.norm(emb_guardado) * np.linalg.norm(emb_actual))
        print(f"🔊 Similitud de voz: {similitud}")

        if similitud > umbral:
            print("✅ Voz reconocida correctamente.")
            return True
        else:
            print("❌ Voz no coincide lo suficiente.")

    print("\n🚫 Se agotaron los intentos. Acceso denegado.")
    return False
