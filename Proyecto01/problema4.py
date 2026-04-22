# Problema 4 – Generación de Audio con el Módulo wave
# Ejecuta este archivo para generar los archivos WAV solicitados
import wave, struct, math

def escala_mono(filename, escala, notas, rate, duration):
    # Esta función crea un archivo WAV mono con las notas de la escala que le digamos.
    AMP = 32767
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for nota in escala:
            freq = notas[nota]
            for i in range(rate * duration):
                sample = int(AMP * math.sin(2 * math.pi * freq / rate * i))
                wf.writeframes(struct.pack('<h', sample))

def escala_stereo(filename, escala, notas, rate, duration):
    # Esta función crea un archivo WAV estéreo con las notas de la escala, igual en ambos canales.
    AMP = 32767
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for nota in escala:
            freq = notas[nota]
            for i in range(rate * duration):
                sample = int(AMP * math.sin(2 * math.pi * freq / rate * i))
                wf.writeframes(struct.pack('<hh', sample, sample))

def onda_compuesta(filename, rate, duration):
    # Esta función crea una onda que mezcla dos frecuencias (500 Hz y 250 Hz) en estéreo.
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        for i in range(rate * duration):
            sample = int(8000 * math.sin(2 * math.pi * 500.0 / rate * i) +
                         8000 * math.sin(2 * math.pi * 250.0 / rate * i))
            wf.writeframes(struct.pack('<hh', sample, sample))

def reducir_volumen(entrada, salida, factor=0.25):
    # Esta función baja el volumen del archivo de entrada y lo guarda con el nuevo volumen.
    with wave.open(entrada, 'r') as wf_in:
        params = wf_in.getparams()
        frames = wf_in.readframes(wf_in.getnframes())
    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    samples_reducidos = [int(s * factor) for s in samples]
    frames_nuevos = struct.pack('<' + 'h' * len(samples_reducidos), *samples_reducidos)
    with wave.open(salida, 'w') as wf_out:
        wf_out.setparams(params)
        wf_out.writeframes(frames_nuevos)

def limpiar_canal_izquierdo(entrada, salida):
    # Esta función pone en cero el canal izquierdo de un archivo estéreo.
    with wave.open(entrada, 'r') as wf_in:
        params  = wf_in.getparams()
        nframes = wf_in.getnframes()
        frames  = wf_in.readframes(nframes)
    samples = list(struct.unpack('<' + 'h' * (len(frames) // 2), frames))
    for i in range(0, len(samples), 2):
        samples[i] = 0
    frames_nuevos = struct.pack('<' + 'h' * len(samples), *samples)
    with wave.open(salida, 'w') as wf_out:
        wf_out.setparams(params)
        wf_out.writeframes(frames_nuevos)

def main():
    # Diccionario con las frecuencias de cada nota
    notas = {
        'Do': 261.63, 'Re': 293.66, 'Mi': 329.63, 'Fa': 349.23,
        'Sol': 392.00, 'La': 440.00, 'Si': 493.88
    }
    escala1 = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si']  # Escala normal
    escala2 = ['Si', 'La', 'Sol', 'Fa', 'Mi', 'Re', 'Do']  # Escala al revés

    print("Generando archivos WAV...")

    # 1. Escala pentatónica Do-Si, mono, 44100 Hz
    escala_mono('escala_44100_mono.wav', escala1, notas, 44100, 1)
    # 2. Escala pentatónica Si-Do, estéreo, 22050 Hz
    escala_stereo('escala_22050_stereo.wav', escala2, notas, 22050, 1)
    # 3. Escala pentatónica Do-Si, mono, 8000 Hz
    escala_mono('escala_8000_mono.wav', escala1, notas, 8000, 1)
    # 4. Onda compuesta estéreo, 44100 Hz, 10 segundos
    onda_compuesta('onda_compuesta.wav', 44100, 10)
    # 5. Bajar el volumen de la onda anterior al 25%
    reducir_volumen('onda_compuesta.wav', 'onda_volumen_bajo.wav', 0.25)
    # 6. Limpiar canal izquierdo (ponerlo en cero)
    limpiar_canal_izquierdo('onda_volumen_bajo.wav', 'onda_sin_canal_izq.wav')

    print("Listo. Analiza los archivos en Audacity.")
    print("\nExplicación de resultados esperados:")
    print("- escala_44100_mono.wav: Se escuchan las notas Do a Si, una por segundo, en buena calidad.")
    print("- escala_22050_stereo.wav: Se escuchan las notas de Si a Do, en estéreo, pero con menos calidad.")
    print("- escala_8000_mono.wav: Igual que la primera, pero suena más feo porque la calidad es baja.")
    print("- onda_compuesta.wav: Es una mezcla de dos sonidos, como un zumbido grave y otro más agudo.")
    print("- onda_volumen_bajo.wav: Es igual que la anterior pero suena mucho más despacio.")
    print("- onda_sin_canal_izq.wav: Solo suena por el lado derecho, el izquierdo está en silencio.")
    print('Abre los archivos en Audacity y mira las formas de onda y el espectro para comparar.')

if __name__ == "__main__":
    main()
