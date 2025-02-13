import tkinter as tk
from menu import *

# Programa principal (main)
def main():
    root = tk.Tk()
    root.geometry("700x600")  # Tamaño de la ventana principal
    ventana_menu(root)  # Llama a la ventana del menú principal
    root.mainloop()

if __name__ == "__main__":
    main()