# Servidor para controlar reproductor multimedia por comandos seriales en Windows
# Requiere pyserial y pywin32 instalados
import serial
import win32api
import win32con
import time

# Virtual Key Codes de Windows para multimedia
TECLAS = {
    'PLAY' : 0xB3,   # VK_MEDIA_PLAY_PAUSE
    'STOP' : 0xB2,   # VK_MEDIA_STOP
    'PAUSE': 0xB3,   # VK_MEDIA_PLAY_PAUSE
    'NEXT' : 0xB0,   # VK_MEDIA_NEXT_TRACK
    'PREV' : 0xB1,   # VK_MEDIA_PREV_TRACK
    'VOL+': 0xAF,    # VK_VOLUME_UP
    'VOL-': 0xAE     # VK_VOLUME_DOWN
}

SERIAL_PORT = 'COM1'  # Puerto VSPE para el servidor
BAUDRATE = 9600

def presionar_tecla(vk_code):
    win32api.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        print("Servidor esperando comandos en COM1...")
        while True:
            linea = ser.readline().decode(errors='ignore').strip().upper()
            if linea:
                print(f"Recibido: {linea}")
                if linea in TECLAS:
                    presionar_tecla(TECLAS[linea])
                    print(f"Acción ejecutada: {linea}")
                else:
                    print(f"Comando no reconocido: {linea}")
    except serial.SerialException as e:
        print(f"Error abriendo el puerto serial: {e}\n¿Está el cliente corriendo y el puerto correcto?")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
