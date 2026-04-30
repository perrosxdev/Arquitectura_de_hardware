import numpy as np
import matplotlib.pyplot as plt
import os

FREQ_0 = 1000    # Frecuencia main
FREQ_1 = 50      # Frecuencia Ruido
SAMPLE = 44100   # Muestras por Segundo
S_RATE = 44100.0 # Tasa de Muestreo

def main(save_images=True):
    s_1 = [np.sin(2*np.pi * FREQ_0 * i/S_RATE) for i in range(SAMPLE)] # Onda original (1000 Hz)
    s_2 = [np.sin(2*np.pi * FREQ_1 * i/S_RATE) for i in range(SAMPLE)] # Onda ruido (50 Hz)
    w_1 = np.array(s_1) ; w_2 = np.array(s_2)
    wi2 = w_1 + w_2 #señal original + ruido

    images_dir = os.path.join(os.path.dirname(__file__), 'ImagesRepo')
    os.makedirs(images_dir, exist_ok=True)

    # Mostrar todo en una sola ventana con subplots
    t = np.arange(SAMPLE) / S_RATE
    fig, axs = plt.subplots(4, 1, figsize=(8, 10))
    
    '''  Graficas señales '''

    # Señal original (1000 Hz) - 500 muestras
    axs[0].plot(w_1[:500], color='b')
    axs[0].set_title('Onda Original')
    axs[0].set_ylabel('Amplitud')

    # Señal ruido (50 Hz) - 4000 muestras
    axs[1].plot(w_2[:4000], color='b')
    axs[1].set_title('Onda Ruido')
    axs[1].set_ylabel('Amplitud')

    # Suma de ambas - 500 muestras
    axs[2].plot(wi2[:500], color='b')
    axs[2].set_title('Onda Original + Ruidosa')
    axs[2].set_ylabel('Amplitud')

    # FFT de la suma
    yf = np.fft.fft(wi2)
    xf = np.fft.fftfreq(SAMPLE, 1.0/S_RATE)
    pos = (xf >= 0) & (xf <= 1200)
    axs[3].plot(xf[pos], np.abs(yf[pos]), color='b')
    axs[3].set_title('Frecuencias en las Ondas (FFT)')
    axs[3].set_xlabel('Frecuencia [Hz]')
    axs[3].set_ylabel('Magnitud')
    axs[3].set_xlim(0, 1200)

    plt.tight_layout()
    if save_images:
        plt.savefig(os.path.join(images_dir, 'Problema1_todo_en_ventana.png'))
    plt.show()

if __name__ == '__main__':
    main()
