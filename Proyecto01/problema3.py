# Problema 3 – Control de Reproductor de Audio por Serial
# Este script es solo un ejemplo de cliente (Linux, sin Win32Api)
# Para pruebas reales en Windows, usar pyserial y Win32Api como en el enunciado
#
# Este código sirve para mandar comandos por el puerto serial a otro programa (el servidor).
# El servidor debería estar en Windows y controlar el reproductor de música.
# Aquí solo puedes probar el envío de comandos si tienes los puertos virtuales bien configurados.

import serial

# Cambia los nombres de los puertos según tu sistema y configuración de VSPE
SERIAL_PORT = '/dev/ttyS1'  # Ejemplo para Linux, en Windows sería 'COM2'
BAUDRATE = 9600

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE)
        print("Comandos disponibles: PLAY / STOP / PAUSE / NEXT / PREV / VOL+ / VOL-")
        while True:
            cmd = input("Ingresa comando: ").strip().upper()
            ser.write((cmd + '\n').encode())
    except Exception as e:
        print(f"Error abriendo el puerto serial: {e}")

if __name__ == "__main__":
    main()

# Para el servidor, ver ejemplo en README (requiere Windows)
#
# Explicación de resultados esperados:
# - Si tienes el servidor corriendo y los puertos bien, cuando escribes un comando aquí,
#   el servidor lo recibe y hace la acción (por ejemplo, pausa la música, sube el volumen, etc).
# - Si no tienes el servidor, igual puedes ver que el comando se manda por el puerto serial.
# - Si te sale error de permisos, revisa que tengas acceso al puerto serial o prueba en Windows.
