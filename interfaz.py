import customtkinter
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

root.mainloop()