import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from utils.user_utils import (registrar_usuario, iniciar_sesion, recuperar_por_biometria, centrar_ventana)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Sistema Biométrico")
        self.root.geometry("400x300")

        # Título
        tk.Label(root, text="Sistema Biométrico", font=("Arial", 18, "bold")).pack(pady=20)

        # Botón: Iniciar sesión
        tk.Button(root, text="Iniciar sesión", width=20, height=2, bg="#4CAF50", fg="white", command=self.ventana_login).pack(pady=10)

        # Botón: Registrar nuevo usuario
        tk.Button(root, text="Registrar usuario", width=20, height=2, bg="#2196F3", fg="white", command=self.registrar_usuario).pack(pady=10)

        # Botón: Salir
        tk.Button(root, text="Salir", width=20, height=2, bg="#f44336", fg="white", command=self.root.quit).pack(pady=10)


    def ventana_login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Iniciar sesión")
        login_window.geometry("300x250")
        centrar_ventana(login_window, 300, 250)

        tk.Label(login_window, text="Usuario:").pack(pady=5)
        entry_usuario = tk.Entry(login_window)
        entry_usuario.pack()

        tk.Label(login_window, text="Contraseña:").pack(pady=5)
        entry_contrasena = tk.Entry(login_window, show="*")
        entry_contrasena.pack()

        def verificar_login():
            usuario = entry_usuario.get().strip()
            contrasena = entry_contrasena.get().strip()
            if usuario and contrasena:
                # Aquí podrías verificar usuario/contraseña con una base de datos o archivo
                messagebox.showinfo("Login", f"Intentando iniciar sesión con {usuario}.")
                login_window.destroy()
                iniciar_sesion(usuario, contrasena)
            else:
                messagebox.showwarning("Campos vacíos", "Debes ingresar usuario y contraseña.")

        def olvide_contrasena():
            login_window.destroy()
            recuperar_por_biometria()

        tk.Button(login_window, text="Iniciar sesión", command=verificar_login, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(login_window, text="Olvidé mi contraseña", command=olvide_contrasena, fg="blue").pack()

    def registrar_usuario(self):
        registrar_usuario(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    centrar_ventana(root, 400, 300)
    root.mainloop()
