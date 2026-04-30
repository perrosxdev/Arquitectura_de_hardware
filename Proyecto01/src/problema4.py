import wave
import struct
import numpy as np
import os

def freq_from_semitone_offset(offset):
    return 440.0 * (2.0 ** (offset / 12.0))

def write_mono_wav(path, samples, rate):
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(b''.join(struct.pack('<h', int(s)) for s in samples))

def write_stereo_wav(path, left, right, rate):
    with wave.open(path, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        frames = []
        for l, r in zip(left, right):
            frames.append(struct.pack('<hh', int(l), int(r)))
        wf.writeframes(b''.join(frames))

def tone(freq, duration, rate, amplitude=16000):
    t = np.linspace(0, duration, int(rate*duration), endpoint=False)
    return amplitude * np.sin(2*np.pi*freq*t)

def main():
    out_dir = os.path.join(os.path.dirname(__file__), 'wav_out')
    os.makedirs(out_dir, exist_ok=True)

    # Desplazamientos de semitonos relativos a A4 (440 Hz)
    notes_offsets = {'C4': -9, 'D4': -7, 'E4': -5, 'F4': -4, 'G4': -2, 'A4': 0, 'B4': 2}
    pentatonic = ['C4','D4','E4','F4','G4','A4','B4']

    # 1) Escala pentatónica en mono a 44100 Hz
    RATE = 44100
    for note in pentatonic:
        f = freq_from_semitone_offset(notes_offsets[note])
        s = tone(f, 1.0, RATE)
        nombre_nota = note.replace('C4','Do').replace('D4','Re').replace('E4','Mi').replace('F4','Fa').replace('G4','Sol').replace('A4','La').replace('B4','Si')
        path = os.path.join(out_dir, f'escala_pentatonica_{nombre_nota}_{RATE}Hz_mono.wav')
        write_mono_wav(path, s, RATE)

    # 2) Escala pentatónica invertida en estéreo a 22050 Hz
    RATE = 22050
    rev = list(reversed(pentatonic))
    left = np.concatenate([tone(freq_from_semitone_offset(notes_offsets[n]), 1.0, RATE) for n in rev])
    right = left.copy()
    nombre_notas = '_'.join([n.replace('C4','Do').replace('D4','Re').replace('E4','Mi').replace('F4','Fa').replace('G4','Sol').replace('A4','La').replace('B4','Si') for n in rev])
    path = os.path.join(out_dir, f'escala_pentatonica_invertida_{nombre_notas}_{RATE}Hz_estereo.wav')
    write_stereo_wav(path, left, right, RATE)

    # 3) Escala pentatónica en mono a 8000 Hz
    RATE = 8000
    for note in pentatonic:
        f = freq_from_semitone_offset(notes_offsets[note])
        s = tone(f, 1.0, RATE)
        nombre_nota = note.replace('C4','Do').replace('D4','Re').replace('E4','Mi').replace('F4','Fa').replace('G4','Sol').replace('A4','La').replace('B4','Si')
        path = os.path.join(out_dir, f'escala_pentatonica_{nombre_nota}_{RATE}Hz_mono.wav')
        write_mono_wav(path, s, RATE)

    # 4) Señal combinada estéreo de 10 segundos, RATE=44100
    RATE = 44100
    dur = 10
    s1 = tone(500.0, dur, RATE, amplitude=8000)
    s2 = tone(250.0, dur, RATE, amplitude=8000)
    left = s1 + s2
    right = s1 + s2
    path = os.path.join(out_dir, 'senal_combinada_500Hz_250Hz_10s_44100Hz_estereo.wav')
    write_stereo_wav(path, left, right, RATE)

    # 5) Bajar el volumen en un 75% (multiplicar por 0.25)
    left_q = left * 0.25
    right_q = right * 0.25
    path = os.path.join(out_dir, 'senal_combinada_500Hz_250Hz_10s_44100Hz_estereo_volumen25.wav')
    write_stereo_wav(path, left_q, right_q, RATE)

    # left_zero = np.zeros_like(left)
    # path = os.path.join(out_dir, 'canal_izquierdo_limpio_estereo.wav')
    # write_stereo_wav(path, left_zero, right, RATE)
    
    # 6) Limpiar el canal izquierdo usando FFT y filtro digital
    # FFT
    left_fft = np.fft.fft(left)
    freqs = np.fft.fftfreq(len(left), 1/RATE)
    # Eliminar componentes entre 200 y 600 Hz (ejemplo)
    mask = (np.abs(freqs) > 200) & (np.abs(freqs) < 600)
    left_fft[mask] = 0
    # IFFT para reconstruir la señal
    left_filtered = np.fft.ifft(left_fft).real
    # Filtro digital pasa bajas (ejemplo)
    from scipy.signal import butter, lfilter
    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a
    def lowpass_filter(data, cutoff, fs, order=5):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y
    left_final = lowpass_filter(left_filtered, cutoff=400, fs=RATE, order=6)
    path = os.path.join(out_dir, 'canal_izquierdo_filtrado_fft_pasabajas_estereo.wav')
    write_stereo_wav(path, left_final, right, RATE)

if __name__ == '__main__':
    import struct
    main()
