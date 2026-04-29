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
  limit = min(len(aV), nMAX)
  for i in range(1, limit):
    aF[i] = nA * aV[i] + (1.0 - nA) * aF[i-1]
  return aF

def main(save_images=True):
  images_dir = os.path.join(os.path.dirname(__file__), 'ImagesRepo')
  os.makedirs(images_dir, exist_ok=True)

  # Choose a smoothing factor (nA) for the complementary filter
  nA = 0.02

  for idx, sig in enumerate(aS):
    filt = Filter_Comp(sig, nA)

    plt.figure(figsize=(8,3))
    t = np.arange(len(sig)) / S_RATE
    plt.plot(t[:2000], sig[:2000], '-b', label='Original')
    plt.plot(t[:2000], filt[:2000], '-r', label='Filtrado')
    plt.title(f'Problema2 - Señal {idx} (azul original, rojo filtrada)')
    plt.xlabel('Tiempo [s]')
    plt.legend()
    if save_images:
      plt.tight_layout(); plt.savefig(os.path.join(images_dir, f'Problema2_sig{idx}.png'))
    plt.show()

if __name__ == '__main__':
  main()
