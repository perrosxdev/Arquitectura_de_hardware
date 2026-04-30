import serial #comunicacion por puerto serial (Puerto COM en este caso)
import argparse #para parsear argumentos, como el puerto y el comando a enviar (facilidad de escritura y lectura)

def send_command(port, cmd, baud=9600):
    try:
        with serial.Serial(port, baud, timeout=1) as s:
            s.write((cmd + '\n').encode('utf-8'))
            print(f'Enviado "{cmd}" a {port}')
    except Exception as e:
        print('Error enviando comando:', e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default='COM6', help='Puerto COM a usar (ej: COM6)')
    parser.add_argument('cmd', help='Comando a enviar (PLAY, STOP, NEXT, PREV, VOL+, VOL-)')
    args = parser.parse_args()
    send_command(args.port, args.cmd)
