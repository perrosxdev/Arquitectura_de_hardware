# Problema 3 – Control de Reproductor de Audio por Serial

# Cliente para enviar comandos por serial en Windows (usar con server.py)
# Asegúrate de tener pyserial instalado y VSPE configurado con COM1 <-> COM2

import serial

# Cambia los nombres de los puertos según tu sistema y configuración de VSPE

# En Windows, usa COM2 (o el puerto que configuraste en VSPE)
SERIAL_PORT = 'COM2'
BAUDRATE = 9600


def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        print("Comandos disponibles: PLAY / STOP / PAUSE / NEXT / PREV / VOL+ / VOL-")
        while True:
            cmd = input("Ingresa comando: ").strip().upper()
            if cmd:
                ser.write((cmd + '\n').encode())
    except serial.SerialException as e:
        print(f"Error abriendo el puerto serial: {e}\n¿Está el servidor corriendo y el puerto correcto?")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()

# Para el servidor, ver ejemplo en README (requiere Windows)
#
# Explicación de resultados esperados:
# - Si tienes el servidor corriendo y los puertos bien, cuando escribes un comando aquí,
#   el servidor lo recibe y hace la acción (por ejemplo, pausa la música, sube el volumen, etc).
# - Si no tienes el servidor, igual puedes ver que el comando se manda por el puerto serial.
# - Si te sale error de permisos, revisa que tengas acceso al puerto serial o prueba en Windows.
