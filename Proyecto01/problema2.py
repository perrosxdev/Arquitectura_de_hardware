# Problema 2 – Filtro Complementario con Matplotlib
# Ejecuta este archivo para resolver el problema 2 de laboratorio
#
# Este código crea tres señales mezclando ondas y luego les aplica un filtro complementario.
# El filtro sirve para "suavizar" la señal, como si le quitara los cambios bruscos.

import numpy as np
import matplotlib.pyplot as plt

FREQ_0 = 9000
FREQ_1 = 5000
FREQ_2 = 100
SAMPLE = 20000
S_RATE = 20000.0
nMAX   = 20000

# Generar las ondas
aW = [
    [2*np.sin(2*np.pi * FREQ_0 * i/S_RATE) for i in range(SAMPLE)],
    [3*np.sin(2*np.pi * FREQ_1 * i/S_RATE) for i in range(SAMPLE)],
    [9*np.sin(2*np.pi * FREQ_2 * i/S_RATE) for i in range(SAMPLE)]
]
# Mezclar para hacer señales más "complicadas"
aS = [
    np.array(aW[0]) + np.array(aW[1]),
    np.array(aW[0]) + np.array(aW[2]),
    np.array(aW[1]) * np.array(aW[2])
]

# Filtro complementario (suaviza la señal)
def Filter_Comp(aV, nA):
    aF = np.zeros(nMAX)
    aF[0] = aV[0]
    for i in range(1, nMAX):
        aF[i] = nA * aV[i] + (1.0 - nA) * aF[i-1]
    return aF

nA = 0.1  # Si lo subes, la señal se suaviza menos
fig, axs = plt.subplots(3, 1, figsize=(12, 10))
titulos = ["Signal 1", "Signal 2", "Signal 3"]
for idx in range(3):
    filtrada = Filter_Comp(aS[idx], nA)
    axs[idx].plot(aS[idx][:200], color='blue', label='Original')
    axs[idx].plot(filtrada[:200], color='red', label='Filtro Complementario')
    axs[idx].set_title(titulos[idx])
    axs[idx].legend()
plt.tight_layout()
plt.show()

# Explicación de resultados esperados:
# - En azul está la señal original, que se ve "loca" o con muchos picos.
# - En rojo está la señal filtrada, que es más suave y sigue la forma general.
# - Si cambias el valor de nA, el filtro cambia: si es más chico, la roja es más suave todavía.
# Esto sirve para quitar ruido o cosas raras de una señal.
