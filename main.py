import tkinter as tk
from tkinter import messagebox

# Ventana del menú principal
def ventana_menu(root):
    # Limpiar la ventana existente
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title("Menú Principal")
    root.configure(bg="#007935")  # Color verde de fondo
    
    # Título
    titulo = tk.Label(root, text="TRADUCTOR DE LENGUAJE DE SEÑAS VENEZOLANO EDUCATIVO",
                      bg="#37B4E3", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    titulo.pack(pady=30)

    # Botón "Iniciar"
    btn_iniciar = tk.Button(root, text="INICIAR", bg="#37B4E3", fg="white",
                            font=("Arial", 12, "bold"), command=lambda: ventana_traductor(root))
    btn_iniciar.pack(pady=10)

    # Botón "Sobre la Aplicación"
    btn_sobre = tk.Button(root, text="SOBRE LA APLICACION", bg="#37B4E3", fg="white",
                          font=("Arial", 12, "bold"), command=lambda: ventana_informacion(root))
    btn_sobre.pack(pady=10)

    # Botón "Salir"
    btn_salir = tk.Button(root, text="SALIR", bg="#EC0D0D", fg="white",
                          font=("Arial", 12, "bold"), command=root.quit)
    btn_salir.pack(pady=30)

#Ventana del traductor
def ventana_traductor(root):
    # Limpiar la ventana existente
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Traductor de Lenguaje de Señas Venezolano Educativo")
    root.configure(bg="#007935")  # Color verde de fondo

    # Título
    titulo = tk.Label(root, text="TRADUCTOR DE LENGUAJE DE SEÑAS VENEZOLANO EDUCATIVO",
                      bg="#37B4E3", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    titulo.pack(pady=30)

    # Botón "Salir"
    btn_salir = tk.Button(root, text="SALIR", bg="#EC0D0D", fg="white",
                          font=("Arial", 12, "bold"), command=root.quit)
    btn_salir.pack(pady=30)

# Ventana de información sobre la aplicación
def ventana_informacion(root):
    # Limpiar la ventana existente
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Información de la Aplicación")
    root.configure(bg="#007935")  # Color verde de fondo

    # Título
    titulo = tk.Label(root, text="TRADUCTOR DE LENGUAJE DE SEÑAS VENEZOLANO EDUCATIVO",
                      bg="#37B4E3", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    titulo.pack(pady=20)

    # Texto informativo
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
    info_label = tk.Label(root, text=texto_info, bg="#37B4E3", fg="white",
                          font=("Arial", 10), justify="left", wraplength=600, padx=15, pady=15)
    info_label.pack(pady=20)

    # Botones
    botones_frame = tk.Frame(root, bg="#007935")
    botones_frame.pack(pady=20)

    # Botón "Volver al Menú"
    btn_volver = tk.Button(botones_frame, text="VOLVER AL MENÚ", bg="#37B4E3", fg="white",
                           font=("Arial", 12, "bold"), width=20, command=lambda: ventana_menu(root))
    btn_volver.grid(row=0, column=0, padx=10)

    # Botón "Salir"
    btn_salir = tk.Button(botones_frame, text="SALIR", bg="#EC0D0D", fg="white",
                          font=("Arial", 12, "bold"), width=20, command=root.quit)
    btn_salir.grid(row=0, column=1, padx=10)

# Programa principal (main)
def main():
    root = tk.Tk()
    root.geometry("700x600")  # Tamaño de la ventana principal
    ventana_menu(root)  # Llama a la ventana del menú principal
    root.mainloop()

if __name__ == "__main__":
    main()
