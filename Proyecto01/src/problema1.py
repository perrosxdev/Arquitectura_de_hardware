import numpy as np
import matplotlib.pyplot as plt
import os

FREQ_0 = 1000    # Frecuencia main
FREQ_1 = 50      # Frecuencia Ruido
SAMPLE = 44100   # Muestras por Segundo
S_RATE = 44100.0 # Tasa de Muestreo

def main(save_images=True):
    s_1 = [np.sin(2*np.pi * FREQ_0 * i/S_RATE) for i in range(SAMPLE)]
    s_2 = [np.sin(2*np.pi * FREQ_1 * i/S_RATE) for i in range(SAMPLE)]
    w_1 = np.array(s_1) ; w_2 = np.array(s_2)
    wi2 = w_1 + w_2

    images_dir = os.path.join(os.path.dirname(__file__), 'ImagesRepo')
    os.makedirs(images_dir, exist_ok=True)

    # Time domain (show first 0.05s)
    t = np.arange(SAMPLE) / S_RATE
    plt.figure(figsize=(8,3))
    plt.plot(t[:2205], wi2[:2205])
    plt.title('Señal combinada en dominio del tiempo (primeros 0.05 s)')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'Problema1_time.png'))
    plt.show()

    # FFT
    yf = np.fft.fft(wi2)
    xf = np.fft.fftfreq(SAMPLE, 1.0/S_RATE)
    pos = xf >= 0

    plt.figure(figsize=(8,3))
    plt.plot(xf[pos], np.abs(yf[pos]))
    plt.title('FFT - Magnitud')
    plt.xlabel('Frecuencia [Hz]')
    plt.xlim(0, 2000)
    plt.ylabel('Magnitud')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'Problema1_fft.png'))
    plt.show()

if __name__ == '__main__':
    main()
