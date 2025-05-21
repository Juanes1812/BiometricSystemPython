from tkinter import simpledialog, messagebox
import tkinter as tk
import cv2
import os
from utils.speech_utils import (registrar_voz, reconocer_voz)
from utils.face_utils import (registrar_foto, reconocer_rostro)



    # Archivo donde guardaremos los usuarios
    
    
def guardar_usuario(nombre, contrasena):
    ARCHIVO_USUARIOS = os.path.join("data", "usuarios.txt")
    with open(ARCHIVO_USUARIOS, "a") as f:
        f.write(f"{nombre},{contrasena}\n")

def usuario_existe(nombre):
    ARCHIVO_USUARIOS = os.path.join("data", "usuarios.txt")
    if not os.path.exists(ARCHIVO_USUARIOS):
        return False
    with open(ARCHIVO_USUARIOS, "r") as f:
        for linea in f:
            if linea.strip().split(",")[0] == nombre:
                return True
    return False

def obtener_contrasena(nombre):
    ARCHIVO_USUARIOS = os.path.join("data", "usuarios.txt")
    if not os.path.exists(ARCHIVO_USUARIOS):
        return None
    with open(ARCHIVO_USUARIOS, "r") as f:
        for linea in f:
            user, pwd = linea.strip().split(",", 1)
            if user == nombre:
                return pwd
    return None

def registrar_usuario(root):
    nombre = simpledialog.askstring("Registrar usuario", "Ingresa el nombre del nuevo usuario:")
    if not nombre:
        messagebox.showwarning("Registro cancelado", "⚠️ Debes ingresar un nombre válido.")
        return

    if usuario_existe(nombre):
        messagebox.showerror("Registro fallido", "❌ El usuario ya existe.")
        return
    # Aquí puedes agregar lógica adicional antes de registrar al usuario
    contrasena = simpledialog.askstring("Contraseña", f"Ingrese una contraseña para {nombre}:", show="*")
    if not contrasena:
        messagebox.showwarning("Registro cancelado", "⚠️ Debes ingresar una contraseña.")
        return
    
    registrar_foto(nombre)
    registrar_voz(nombre, root=root)
    guardar_usuario(nombre, contrasena)
    print("🎉 Registro completo.")
    messagebox.showinfo("Registro", f"🎉 Usuario {nombre} registrado con éxito.")

def iniciar_sesion(nombre, contrasena):
    if not nombre or not contrasena:
        messagebox.showwarning("Inicio cancelado", "⚠️ Debes ingresar usuario y contraseña.")
        return False

    if not usuario_existe(nombre):
        messagebox.showerror("Error", "❌ El usuario no existe.")
        return False

    contrasena_guardada = obtener_contrasena(nombre)
    if contrasena_guardada is None:
        messagebox.showerror("Error", "❌ No se pudo obtener la contraseña del usuario.")
        return False

    if contrasena == contrasena_guardada:
        messagebox.showinfo("Inicio de sesión", f"✅ Bienvenido, {nombre}!")
        return True
    else:
        messagebox.showerror("Error", "❌ Contraseña incorrecta.")
        return False

# Método para recuperar la contraseña usando biometría
def recuperar_por_biometria():
    nombre = reconocer_rostro()
    if nombre:
        messagebox.showinfo("Reconocimiento Facial", f"Rostro reconocido: {nombre}")
        if reconocer_voz(nombre):
            messagebox.showinfo("Recuperación", f"✅ Identidad verificada. Bienvenido, {nombre}!")
        else:
            messagebox.showerror("Error", "❌ Voz no reconocida.")
    else:
        messagebox.showerror("Error", "❌ Rostro no reconocido.")

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
