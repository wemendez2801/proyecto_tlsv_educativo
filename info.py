import tkinter as tk
from tkinter import messagebox

# Función para el botón de "Salir"
def salir():
    root.destroy()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Información de la Aplicación")
root.configure(bg="#007935")  # Color verde de fondo
root.geometry("800x500")  # Tamaño de la ventana

# Título
titulo = tk.Label(root, text="TRADUCTOR DE LENGUAJE DE SEÑAS VENEZOLANO EDUCATIVO",
                  bg="#37B4E3", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
titulo.pack(pady=20)

# Marco de texto informativo
texto_info = (
    "Esta aplicación ha sido diseñada como una herramienta inclusiva que facilita la\n"
    "comunicación entre estudiantes con discapacidades del habla en el entorno educativo,\n"
    "utilizando como base el Lenguaje de Señas Venezolano (LSV). La aplicación emplea\n"
    "tecnología de inteligencia artificial y visión por computadora para identificar las señas\n"
    "realizadas por el usuario y traducirlas en tiempo real mediante texto en pantalla. Se permite\n"
    "una interacción más efectiva y accesible dentro de aulas de clase y otros contextos educativos.\n\n"
    "El principal objetivo de esta herramienta es promover la inclusión educativa,\n"
    "ofreciendo a estudiantes con discapacidades del habla la oportunidad de participar de manera\n"
    "activa en el proceso de aprendizaje. Con ello, se busca reducir barreras y fomentar una\n"
    "integración plena dentro del entorno académico.\n\n"
    "Esta aplicación es el resultado de un proyecto de trabajo de grado desarrollado para la\n"
    "carrera de Ingeniería Informática de la Universidad Católica Andrés Bello. Su diseño refleja\n"
    "el compromiso con la innovación tecnológica y la creación de soluciones que contribuyan al\n"
    "bienestar social y la equidad educativa en Venezuela."
)

# Cuadro de texto informativo
info_label = tk.Label(root, text=texto_info, bg="#37B4E3", fg="white",
                      font=("Arial", 10), justify="left", wraplength=600, padx=15, pady=15)
info_label.pack(pady=20)

# Botones
botones_frame = tk.Frame(root, bg="#007935")
botones_frame.pack(pady=20)

# Botón "Iniciar"
btn_iniciar = tk.Button(botones_frame, text="INICIAR", bg="#37B4E3", fg="white",
                        font=("Arial", 12, "bold"), width=15, command=lambda: messagebox.showinfo("Iniciar", "La aplicación está iniciando..."))
btn_iniciar.grid(row=0, column=0, padx=10)

# Botón "Salir"
btn_salir = tk.Button(botones_frame, text="SALIR", bg="#EC0D0D", fg="white",
                      font=("Arial", 12, "bold"), width=15, command=salir)
btn_salir.grid(row=0, column=1, padx=10)

# Iniciar el bucle principal
root.mainloop()
