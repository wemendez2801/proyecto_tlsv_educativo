import tkinter as tk
from tkinter import messagebox

# Funciones para los botones
def iniciar():
    messagebox.showinfo("Iniciar", "La aplicación está iniciando...")

def sobre_aplicacion():
    messagebox.showinfo("Sobre la Aplicación", "Traductor de Lenguaje de Señas Venezolano Educativo.\nVersión 1.0")

def salir():
    root.destroy()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Traductor de Lenguaje de Señas Venezolano Educativo")
root.configure(bg="#007935")  # Color verde de fondo
root.geometry("800x500")  # Tamaño de la ventana

# Título
titulo = tk.Label(root, text="TRADUCTOR DE LENGUAJE DE SEÑAS VENEZOLANO EDUCATIVO",
                  bg="#37B4E3", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
titulo.pack(pady=30)

# Botón "Iniciar"
btn_iniciar = tk.Button(root, text="INICIAR", bg="#37B4E3", fg="white",
                        font=("Arial", 12, "bold"), command=iniciar)
btn_iniciar.pack(pady=10)

# Botón "Sobre la Aplicación"
btn_sobre = tk.Button(root, text="SOBRE LA APLICACION", bg="#37B4E3", fg="white",
                      font=("Arial", 12, "bold"), command=sobre_aplicacion)
btn_sobre.pack(pady=10)

# Botón "Salir"
btn_salir = tk.Button(root, text="SALIR", bg="#EC0D0D", fg="white",
                      font=("Arial", 12, "bold"), command=salir)
btn_salir.pack(pady=30)

# Iniciar el bucle principal
root.mainloop()

""" import customtkinter
import tkinter as tk

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("500x350")

def login():
    print("Test")



frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Traductor de Lenguaje de Señas Venezolano Educativo")
label.pack(pady=12 , padx=10)

button = customtkinter.CTkButton(master=frame, fg_color="blue", text="Iniciar")
button.pack(pady=12,padx=10)

button = customtkinter.CTkButton(master=frame, fg_color="blue", text="Sobre la aplicación")
button.pack(pady=12,padx=10)

button = customtkinter.CTkButton(master=frame, fg_color="red", text="Salir")
button.pack(pady=12,padx=10)

root.mainloop() """