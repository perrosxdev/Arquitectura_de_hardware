# Interfaz gráfica para laboratorio de Arquitectura de Hardware
# Ejecuta los problemas desde una sola ventana
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

ARCHIVOS = [
    ("Problema 1 – FFT con NumPy", "problema1.py"),
    ("Problema 2 – Filtro Complementario", "problema2.py"),
    ("Problema 3 – Control Serial (cliente)", "problema3.py"),
    ("Problema 4 – Generación de Audio", "problema4.py"),
]

RUTA = os.path.dirname(os.path.abspath(__file__))

def ejecutar_script(nombre):
    ruta = os.path.join(RUTA, nombre)
    if not os.path.exists(ruta):
        messagebox.showerror("Error", f"No se encontró el archivo: {nombre}")
        return
    try:
        subprocess.Popen([sys.executable, ruta])
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Laboratorio Arquitectura de Hardware")
root.geometry("400x350")

label = tk.Label(root, text="Selecciona el problema a ejecutar:", font=("Arial", 14))
label.pack(pady=20)

for texto, archivo in ARCHIVOS:
    btn = tk.Button(root, text=texto, width=40, height=2, command=lambda f=archivo: ejecutar_script(f))
    btn.pack(pady=5)

root.mainloop()
