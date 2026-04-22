w12 = w_1 + w_2
# Problema 1 – FFT con NumPy
# Ejecuta este archivo para resolver el problema 1 de laboratorio
#
# Este código genera dos ondas: una principal (1000 Hz) y una de ruido (50 Hz).
# Después las suma y muestra las gráficas de cada una y la suma.
# Al final, hace la FFT para ver qué frecuencias hay en la señal mezclada.

import numpy as np
import matplotlib.pyplot as plt

FREQ_0 = 1000    # Frecuencia principal
FREQ_1 = 50      # Frecuencia de ruido
SAMPLE = 44100   # Muestras por segundo
S_RATE = 44100.0 # Tasa de muestreo

# Generar las ondas
s_1 = [np.sin(2*np.pi * FREQ_0 * i/S_RATE) for i in range(SAMPLE)]  # 1000 Hz
s_2 = [np.sin(2*np.pi * FREQ_1 * i/S_RATE) for i in range(SAMPLE)]  # 50 Hz
w_1 = np.array(s_1)
w_2 = np.array(s_2)
w12 = w_1 + w_2

# Hacemos la FFT para ver las frecuencias
fft_result = np.fft.fft(w12)
fft_freq   = np.fft.fftfreq(len(w12), d=1/S_RATE)

# Graficar todo
fig, axs = plt.subplots(4, 1, figsize=(12, 10))
axs[0].plot(w_1[:500])
axs[0].set_title("Onda Original (1000 Hz)")
axs[1].plot(w_2[:4000])
axs[1].set_title("Onda Ruido (50 Hz)")
axs[2].plot(w12[:3000])
axs[2].set_title("Onda Original + Ruido")
axs[3].plot(fft_freq[:len(fft_freq)//2], np.abs(fft_result)[:len(fft_result)//2])
axs[3].set_title("Frecuencias en la Señal (FFT)")
plt.tight_layout()
plt.show()

# Explicación de resultados esperados:
# - En la primera gráfica se ve la onda limpia de 1000 Hz (parece una onda normal).
# - En la segunda, la de 50 Hz, que es más lenta.
# - En la tercera, la suma, se ve como una onda "gorda" porque tiene las dos mezcladas.
# - En la última, la FFT, aparecen dos picos grandes: uno en 50 Hz y otro en 1000 Hz, que son las frecuencias que metimos.
# Si ves eso, ¡todo está bien!
