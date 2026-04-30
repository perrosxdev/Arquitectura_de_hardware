import time
import argparse
from problema3_cliente import send_command

DEFAULT_COMMANDS = ['PLAY', 'VOL+', 'VOL+', 'VOL-', 'NEXT', 'PREV', 'STOP']

def ciclo_comandos(port: str, commands, intervalo: float, vueltas: int):
    print(f'Iniciando envíos a {port}: {commands} cada {intervalo}s ({vueltas} vueltas)')
    for v in range(vueltas):
        for cmd in commands:
            send_command(port, cmd)
            time.sleep(intervalo)
    print('Secuencia de comandos finalizada')


def main():
    parser = argparse.ArgumentParser(description='Envía comandos serial periódicos para probar el servidor')
    parser.add_argument('--port', default='COM6', help='Puerto COM a usar (ej: COM6)')
    parser.add_argument('--interval', type=float, default=1.0, help='Segundos entre comandos')
    parser.add_argument('--loops', type=int, default=1, help='Cantidad de pasadas sobre la lista de comandos')
    parser.add_argument('--commands', nargs='*', default=DEFAULT_COMMANDS, help='Lista de comandos a enviar')
    args = parser.parse_args()

    try:
        ciclo_comandos(args.port, args.commands, args.interval, args.loops)
    except KeyboardInterrupt:
        print('\nEnvío interrumpido por usuario')


if __name__ == '__main__':
    main()
