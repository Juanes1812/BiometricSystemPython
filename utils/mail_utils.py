import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import simpledialog, messagebox
from dotenv import load_dotenv


load_dotenv()
remitente = os.getenv("CORREO")
clave = os.getenv("CLAVE")

ARCHIVO_USUARIOS = os.path.join("data", "usuarios.txt")

def obtener_correo_por_nombre(nombre_usuario):
    with open(ARCHIVO_USUARIOS, "r") as f:
        for linea in f:
            datos = linea.strip().split(",")
            if datos[0] == nombre_usuario and len(datos) >= 3:
                return datos[2]
    return None



def generar_codigo_verificacion(longitud=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=longitud))



def enviar_correo_verificacion(destinatario, codigo, remitente, clave):
    asunto = "Código de Verificación"
    cuerpo = f"Tu código de verificación es: {codigo}"

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remitente, clave)
            servidor.send_message(mensaje)
        return True
    except Exception as e:
        messagebox.showerror("Correo", f"❌ Error al enviar correo: {e}")
        return False



def verificar_usuario_por_correo(nombre_usuario):
    correo = obtener_correo_por_nombre(nombre_usuario)
    if not correo:
        messagebox.showerror("Error", "❌ No se encontró el correo del usuario.")
        return

    codigo = generar_codigo_verificacion()
    if enviar_correo_verificacion(correo, codigo, remitente, clave):
        ingreso = simpledialog.askstring("Verificación", "Ingresa el código que recibiste por correo:")
        if ingreso == codigo:
            messagebox.showinfo("Éxito", "✅ Verificación completada.")
            return True
        else:
            messagebox.showerror("Error", "❌ Código incorrecto.")
            return False
