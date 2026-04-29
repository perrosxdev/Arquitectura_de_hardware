import threading
import tkinter as tk
from tkinter import messagebox
import os

ROOT = os.path.dirname(__file__)
import problema1
import problema2
import problema4
import problema3_server
import problema3_cliente

server_thread = None

def run_problem1():
    threading.Thread(target=problema1.main, daemon=True).start()

def run_problem2():
    threading.Thread(target=problema2.main, daemon=True).start()

def run_problem4():
    threading.Thread(target=problema4.main, daemon=True).start()

def start_server(port):
    def target():
        problema3_server.run_server(port)
    global server_thread
    if server_thread and server_thread.is_alive():
        messagebox.showinfo('Server', 'Servidor ya está en ejecución')
        return
    server_thread = threading.Thread(target=target, daemon=True)
    server_thread.start()
    messagebox.showinfo('Server', f'Servidor iniciado en {port} (ver consola)')

def send_cmd(port, cmd):
    threading.Thread(target=problema3_cliente.send_command, args=(port, cmd), daemon=True).start()

def build_gui():
    root = tk.Tk()
    root.title('Proyecto01 - Panel')

    frm = tk.Frame(root, padx=10, pady=10)
    frm.pack()

    tk.Label(frm, text='Problemas (ejecutar)').pack()
    tk.Button(frm, text='Problem 1 (FFT)', width=20, command=run_problem1).pack(pady=2)
    tk.Button(frm, text='Problem 2 (Filtro)', width=20, command=run_problem2).pack(pady=2)
    tk.Button(frm, text='Problem 4 (WAV)', width=20, command=run_problem4).pack(pady=2)

    tk.Label(frm, text='\nProblema 3 - Control Reproductor (cliente/servidor)').pack()
    port_frame = tk.Frame(frm)
    port_frame.pack()
    tk.Label(port_frame, text='COM servidor:').pack(side='left')
    port_entry = tk.Entry(port_frame)
    port_entry.insert(0, 'COM5')
    port_entry.pack(side='left')
    tk.Button(port_frame, text='Start Server', command=lambda: start_server(port_entry.get())).pack(side='left', padx=5)

    btns = tk.Frame(frm)
    btns.pack(pady=6)
    tk.Button(btns, text='PLAY', width=8, command=lambda: send_cmd(port_entry.get(), 'PLAY')).grid(row=0,column=0,padx=3,pady=2)
    tk.Button(btns, text='STOP', width=8, command=lambda: send_cmd(port_entry.get(), 'STOP')).grid(row=0,column=1,padx=3)
    tk.Button(btns, text='NEXT', width=8, command=lambda: send_cmd(port_entry.get(), 'NEXT')).grid(row=0,column=2,padx=3)
    tk.Button(btns, text='PREV', width=8, command=lambda: send_cmd(port_entry.get(), 'PREV')).grid(row=0,column=3,padx=3)
    tk.Button(btns, text='VOL+', width=8, command=lambda: send_cmd(port_entry.get(), 'VOL+')).grid(row=1,column=0,padx=3,pady=2)
    tk.Button(btns, text='VOL-', width=8, command=lambda: send_cmd(port_entry.get(), 'VOL-')).grid(row=1,column=1,padx=3)

    root.mainloop()

if __name__ == '__main__':
    build_gui()
