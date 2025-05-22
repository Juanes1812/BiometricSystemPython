import tkinter as tk
from tkinter import  messagebox
from utils.user_utils import (registrar_usuario, iniciar_sesion, recuperar_por_biometria, centrar_ventana)
from utils.mail_utils import (verificar_usuario_por_correo)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Sistema Biométrico")
        self.root.geometry("400x300")

        tk.Label(root, text="Sistema Biométrico", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(root, text="Iniciar sesión", width=20, height=2, bg="#9F6BA0", fg="white", command=self.ventana_login).pack(pady=10)
        tk.Button(root, text="Registrar usuario", width=20, height=2, bg="#C880B7", fg="white", command=self.registrar_usuario).pack(pady=10)
        tk.Button(root, text="Salir", width=20, height=2, bg="#4A2040", fg="white", command=self.root.quit).pack(pady=10)


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
                
                messagebox.showinfo("Login", f"Intentando iniciar sesión con {usuario}.")
                login_window.destroy()
                if iniciar_sesion(usuario, contrasena):
                    messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso para {usuario}")
                    login_window.destroy()
                    self.mostrar_pagina_principal(usuario)
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

            else:
                messagebox.showwarning("Campos vacíos", "Debes ingresar usuario y contraseña.")

        def olvide_contrasena():
            login_window.destroy()
            recuperar_por_biometria()

        def olvide_contrasena():
            login_window.destroy()
            exito, nombre_usuario = recuperar_por_biometria()
            if exito:
                self.mostrar_pagina_principal(nombre_usuario)
            else:   
                messagebox.showerror("Error", "No se pudo recuperar la cuenta.")

        tk.Button(login_window, text="Iniciar sesión", command=verificar_login, bg="#9F6BA0", fg="white").pack(pady=10)
        tk.Button(login_window, text="Olvidé mi contraseña", command=olvide_contrasena, fg="purple").pack()

    def registrar_usuario(self):
        registrar_usuario(self.root)

    def verificar_por_correo(self):
        verificar_usuario_por_correo(self.root)

    def mostrar_pagina_principal(self, nombre_usuario):
        ventana_principal = tk.Toplevel(self.root)
        ventana_principal.title("Bienvenido")
        ventana_principal.geometry("400x300")
        centrar_ventana(ventana_principal, 400, 300)

        tk.Label(ventana_principal, text=f"¡Bienvenido, {nombre_usuario}!", font=("Arial", 16)).pack(pady=30)
        tk.Label(ventana_principal, text="Ya, eso fue todo, ahora ¡vuelve a salir!", font=("Arial", 12)).pack(pady=30)

        tk.Button(ventana_principal, text="Cerrar sesión", bg="#4A2040", fg="white", command=ventana_principal.destroy).pack(pady=20)



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    centrar_ventana(root, 400, 300)
    root.mainloop()
