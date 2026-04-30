import wave
import struct
import math
import os
from scipy.signal import resample_poly

AMPLITUD = 16000          # Amplitud máxima (16-bit: máx 32767)
DURACION_NOTA = 1.0       # Cada nota dura 1 segundo

# Escala pentatónica mayor de Do: 5 notas
# Frecuencias exactas usando la fórmula: f = 440 * 2^(semitono/12)
NOTAS = {
    'Do4': 440.0 * (2 ** (-9 / 12)),
    'Re4': 440.0 * (2 ** (-7 / 12)), 
    'Mi4': 440.0 * (2 ** (-5 / 12)),
    # 'Fa4': 440.0 * (2 ** (-4 / 12)),
    'Sol4': 440.0 * (2 ** (-2 / 12)),
    'La4': 440.0 * (2 ** ( 0 / 12)),   
    # 'Si4': 440.0 * (2 ** ( 2 / 12)),  
}

# ASCENDENTE  = ['Do4', 'Re4', 'Mi4', 'Fa4', 'Sol4', 'La4', 'Si4']
# DESCENDENTE = ['Si4', 'La4', 'Sol4', 'Fa4', 'Mi4', 'Re4', 'Do4']

# Orden ascendente y descendente
ASCENDENTE  = ['Do4', 'Re4', 'Mi4', 'Sol4', 'La4']
DESCENDENTE = ['La4', 'Sol4', 'Mi4', 'Re4', 'Do4']

CARPETA = 'wav_out'
os.makedirs(CARPETA, exist_ok=True)

# Si se usa decimacion se debe cambiar la decimacion a 441 para que funcione limpio

# def generar_muestras(frecuencia: float, duracion: float, tasa: int, decimacion: int = 2, amplitud: float = AMPLITUD) -> list[int]:
#     """
#     Genera una lista de muestras PCM 16-bit para una onda senoidal y aplica decimación.
#     Decimación: solo se toma 1 de cada N muestras (N=decimacion).
#     """
#     n_muestras = int(tasa * duracion)
#     muestras = [
#         int(amplitud * math.sin(2 * math.pi * frecuencia * i / tasa))
#         for i in range(n_muestras)
#     ]
#     decimadas = resample_poly(muestras, up=80, down=decimacion)
#     return [int(m) for m in decimadas]

def generar_muestras(frecuencia: float, duracion: float, tasa: int,
                     amplitud: float = AMPLITUD) -> list[int]:
    # Calcular las muestras para la tasa correspondiente
    n_muestras = int(tasa * duracion)
    return [
        #Convertimos el numero de muestras en tiempo real (segundos)
        int(amplitud * math.sin(2 * math.pi * frecuencia * i / tasa))
        #Repetimos para cada muestra
        for i in range(n_muestras)
    ]


def escribir_mono(ruta: str, muestras: list[int], tasa: int) -> None:

    #abrir wav en modo escritura 
    with wave.open(ruta, 'w') as f:
        f.setnchannels(1)   # Mono
        f.setsampwidth(2)   # 2 bytes por muestra = 16 bits
        f.setframerate(tasa) # Frames por segundo
        datos = b''.join(struct.pack('<h', m) for m in muestras) # cada numero entero en 2 bytes ordenados en little endian y el entero debe ser de 16 bits (h)
        f.writeframes(datos)
    print(f'  [OK] {ruta}  ({len(muestras)} muestras, {tasa} Hz, mono)')


def escribir_estereo(ruta: str, izq: list[int], der: list[int],
                     tasa: int) -> None:
    """
    En formato WAV estéreo, las muestras se intercalan: [L, R, L, R, ...]
    struct.pack('<hh', l, r) empaqueta ambos canales en 4 bytes por frame.
    """
    #abrir wav en modo escritura
    with wave.open(ruta, 'w') as f:
        f.setnchannels(2) # Estéreo
        f.setsampwidth(2) # 2 bytes por muestra
        f.setframerate(tasa) # Frames por segundo
        #empaquetamos dos muestras (izq y der) en un solo frame de 4 bytes, y luego concatenamos
        datos = b''.join(struct.pack('<hh', l, r) for l, r in zip(izq, der))
        #escribimos los frames al archivo
        f.writeframes(datos)
    n = min(len(izq), len(der))
    print(f'  [OK] {ruta}  ({n} frames, {tasa} Hz, estéreo)')


def leer_estereo(ruta: str) -> tuple[list[int], list[int], int]:
    #abrimos y leemos el wav
    with wave.open(ruta, 'r') as f:
        tasa = f.getframerate()
        n_frames = f.getnframes()
        raw = f.readframes(n_frames) # Leemos todos los frames como bytes (cada frame es 4 bytes: 2 para izq y 2 para der)

    izq, der = [], []
    tam_frame = 4  # 2 bytes canal izq + 2 bytes canal der
    for i in range(0, len(raw), tam_frame):
        l, r = struct.unpack('<hh', raw[i:i + tam_frame])
        izq.append(l)
        der.append(r)

    return izq, der, tasa

def main():
    # Escala pentatónica Do-La, 44100 Hz, Mono
    tasa = 44100
    muestras = []
    for nombre in ASCENDENTE:
        muestras += generar_muestras(NOTAS[nombre], DURACION_NOTA, tasa)
    escribir_mono(
        os.path.join(CARPETA, 'escala_pentatonica_DoReMiSolLa_44100Hz_mono.wav'),
        muestras, tasa
    )

    # Escala pentatónica La-Do, 22050 Hz, Estéreo
    tasa = 22050
    muestras = []
    for nombre in DESCENDENTE:
        muestras += generar_muestras(NOTAS[nombre], DURACION_NOTA, tasa)
    escribir_estereo(
        os.path.join(CARPETA, 'escala_pentatonica_LaSolMiReDo_22050Hz_estereo.wav'),
        muestras, muestras, tasa
    )
    # Escala pentatónica Do-La, 8000 Hz, Mono
    tasa = 8000
    muestras = []
    for nombre in ASCENDENTE:
        muestras += generar_muestras(NOTAS[nombre], DURACION_NOTA, tasa)
    escribir_mono(
        os.path.join(CARPETA, 'escala_pentatonica_DoReMiSolLa_8000Hz_mono.wav'),
        muestras, tasa
    )

    # Onda compuesta 500 Hz + 250 Hz, 10s, Estéreo
    tasa = 44100 #Rate
    duracion = 10 
    n = int(tasa * duracion) #Cantidad de muestras totales
    canal = [
        int(8000 * math.sin(2 * math.pi * 500.0 * i / tasa) +
            8000 * math.sin(2 * math.pi * 250.0 * i / tasa))
        for i in range(n)
    ]
    ruta_onda = os.path.join(CARPETA, 'onda_compuesta_500Hz_250Hz_10s_44100Hz_estereo.wav')
    escribir_estereo(ruta_onda, canal, canal, tasa)

    # Volumen al 25% (bajar 75%)
    izq, der, tasa = leer_estereo(ruta_onda)
    izq_bajo = [int(m * 0.25) for m in izq]
    der_bajo = [int(m * 0.25) for m in der]
    ruta_bajo = os.path.join(CARPETA, 'onda_volumen_25pct_44100Hz_estereo.wav')
    escribir_estereo(ruta_bajo, izq_bajo, der_bajo, tasa)

    # Canal izquierdo en silencio (con 0)
    izq2, der2, tasa = leer_estereo(ruta_bajo)
    canal_izq_silencio = [0] * len(izq2)
    ruta_limpio = os.path.join(CARPETA, 'onda_canal_izq_silencio_44100Hz_estereo.wav')
    escribir_estereo(ruta_limpio, canal_izq_silencio, der2, tasa)

# Para ejecución directa y compatibilidad con el GUI
if __name__ == '__main__':
    main()