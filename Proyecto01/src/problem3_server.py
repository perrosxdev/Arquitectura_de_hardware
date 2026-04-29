import serial
import threading
import time
import argparse

try:
    import win32api
except Exception:
    win32api = None

# Virtual-key codes (Win32)
VK = {
    'NEXT': 0xB0,
    'PREV': 0xB1,
    'STOP': 0xB2,
    'PLAYPAUSE': 0xB3,
    'VOL_MUTE': 0xAD,
    'VOL_DOWN': 0xAE,
    'VOL_UP': 0xAF,
}

def press_vk(vk):
    if win32api is None:
        print('win32api no disponible: no se enviarán teclas (ejecutar en Windows con pywin32)')
        return
    win32api.keybd_event(vk, 0, 0, 0)
    time.sleep(0.02)
    win32api.keybd_event(vk, 0, 2, 0)

def handle_command(cmd):
    c = cmd.strip().upper()
    print('Recibido comando:', c)
    if c == 'PLAY':
        press_vk(VK['PLAYPAUSE'])
    elif c == 'STOP':
        press_vk(VK['STOP'])
    elif c == 'NEXT':
        press_vk(VK['NEXT'])
    elif c == 'PREVIOUS' or c == 'PREV':
        press_vk(VK['PREV'])
    elif c == 'VOL+':
        press_vk(VK['VOL_UP'])
    elif c == 'VOL-':
        press_vk(VK['VOL_DOWN'])
    else:
        print('Comando no reconocido:', c)

def run_server(port, baud=9600):
    print(f'Iniciando servidor serial en {port} @ {baud}bps')
    try:
        ser = serial.Serial(port, baud, timeout=1)
    except Exception as e:
        print('No se pudo abrir el puerto serial:', e)
        print('Asegúrate de crear puertos virtuales (VSPE) y asignar el puerto correcto.')
        return

    try:
        while True:
            line = ser.readline()
            if not line:
                continue
            try:
                cmd = line.decode('utf-8', errors='ignore').strip()
            except Exception:
                cmd = str(line)
            if cmd:
                handle_command(cmd)
    except KeyboardInterrupt:
        print('Servidor detenido por usuario')
    finally:
        ser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default='COM5', help='Puerto COM a escuchar (ej: COM5)')
    args = parser.parse_args()
    run_server(args.port)
