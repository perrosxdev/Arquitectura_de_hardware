import numpy as np
import matplotlib.pyplot as plt
import os

FREQ_0 = 9000 ; FREQ_1 = 5000; FREQ_2 = 100  # Frecuencia 1, 2 y 3
SAMPLE = 20000 ; S_RATE = 20000.0 # Samples y Tasa de Muestreo
nMAX = 20000

aW = [
  [2*np.sin(2*np.pi * FREQ_0 * i/S_RATE) for i in range(SAMPLE)],
  [3*np.sin(2*np.pi * FREQ_1 * i/S_RATE) for i in range(SAMPLE)],
  [9*np.sin(2*np.pi * FREQ_2 * i/S_RATE) for i in range(SAMPLE)]
  ]

aS = [
  np.array(aW[0]) + np.array(aW[1]),
  np.array(aW[0]) + np.array(aW[2]),
  np.array(aW[1]) * np.array(aW[2])
  ]

def Filter_Comp(aV, nA):
    aF = np.zeros_like(aV)
    aF[0] = aV[0]
    for i in range(1, nMAX):
        aF[i] = nA * aV[i] + (1.0 - nA) * aF[i-1]
    return aF

def main(save_images=True):
  images_dir = os.path.join(os.path.dirname(__file__), 'ImagesRepo')
  os.makedirs(images_dir, exist_ok=True)
  # Define un nA diferente para cada señal
  nAs = [0.5, 0.6, 0.05]

  # Mostrar las 3 señales en una sola ventana 
  fig, axs = plt.subplots(3, 1, figsize=(9, 7))
  fig.patch.set_facecolor('#bdbdbd')  # fondo gris

  ylims = [(-6, 6), (-15, 15), (-30, 30)]
  titles = ['Signal 1', 'Signal 2', 'Signal 3']

  for idx, sig in enumerate(aS):
    nA = nAs[idx]
    filt = Filter_Comp(sig, nA)
    ax = axs[idx]
    ax.set_facecolor('white')
    muestras = np.arange(200)
    ax.plot(muestras, sig[:200], '-b')
    ax.plot(muestras, filt[:200], '-r', label=f'nA={nA}')
    ax.set_title(titles[idx], pad=6, fontsize=14)
    ax.set_xlim(0, 200)
    ax.set_ylim(ylims[idx])
    ax.tick_params(axis='both', which='both', length=4)
    ax.legend()

  plt.tight_layout()
  if save_images:
    plt.savefig(os.path.join(images_dir, 'Problema2_todas_senales.png'))
  plt.show()
  plt.show()

if __name__ == '__main__':
  main()
