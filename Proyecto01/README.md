# Lab #1 – INFO1155

**Autor del laboratorio:** Alberto Caro  
**Modalidad:** Trabajo individual o en grupo de 2 personas  
**Fecha de entrega y defensa:** Jueves 30 de Abril, desde las 14:00 a 18:00 (en oficina del profesor)

---


## Instrucciones de Uso

### 1. Crear entorno virtual (recomendado)

Desde la carpeta `Proyecto01`, ejecuta en terminal:

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows para powershell: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
# venv\Scripts\activate 

```

### 2. Instalar dependencias

```bash
pip install numpy matplotlib pyserial pywin32
```

> Nota: Para el problema 3 (control de reproductor en Windows) también se requiere `pywin32` y ejecutar en Windows.

### 3. Ejecutar los archivos

Puedes ejecutar cada problema por separado:

```bash
python problema1.py   # FFT con NumPy
python problema2.py   # Filtro Complementario
python problema3.py   # Control Serial (cliente)
python problema4.py   # Generación de audio WAV
```

O puedes lanzar la interfaz gráfica para elegir el problema desde una ventana:

```bash
python interfaz.py
```

---

## Descripción General

Laboratorio orientado al manejo de señales, procesamiento de audio y comunicación serial en Python, aplicando conceptos de Arquitectura de Hardware.

---

## Problema 1 – FFT con NumPy

**Objetivo:** Aplicar la Transformada Rápida de Fourier (FFT) para identificar las frecuencias presentes en una señal.

### Lo que debes hacer:
- Ejecutar el script que genera dos señales senoidales y su suma
- Obtener y mostrar las siguientes gráficas:
  - Onda Original
  - Onda Ruido
  - Onda Original + Ruidosa
  - Frecuencias en las Ondas (FFT)
- **Explicar claramente los resultados obtenidos**

### Código base proporcionado:

> ⚠️ **Este código está INCOMPLETO.** Genera las señales pero le falta la parte de graficar con Matplotlib y calcular la FFT con `numpy.fft`. Debes agregar esa parte tú mismo.

```python
import numpy as np, matplotlib.pyplot as plt

FREQ_0 = 1000    # Frecuencia main
FREQ_1 = 50      # Frecuencia Ruido
SAMPLE = 44100   # Muestras por Segundo
S_RATE = 44100.0 # Tasa de Muestreo

s_1 = [np.sin(2*np.pi * FREQ_0 * i/S_RATE) for i in range(SAMPLE)]  # 1000 Senos c/s
s_2 = [np.sin(2*np.pi * FREQ_1 * i/S_RATE) for i in range(SAMPLE)]  # 50 Senos c/s
w_1 = np.array(s_1) ; w_2 = np.array(s_2)                            # Listas 2 Array
w12 = w_1 + w_2                                                        # Sumamos 2 ondas

# --- LO QUE DEBES AGREGAR ---

# 1. Graficar w_1 (Onda Original)
# 2. Graficar w_2 (Onda Ruido)
# 3. Graficar w12 (Onda Original + Ruidosa)
# 4. Calcular FFT de w12 con np.fft.fft() y graficar las frecuencias
```

**Vista del código y gráfico:**  
![Problema 1 - FFT con NumPy](assets/marca1.png)

### Qué agregar (guía):
```python
# Calcular FFT
fft_result = np.fft.fft(w12)
fft_freq   = np.fft.fftfreq(len(w12), d=1/S_RATE)

# Graficar
fig, axs = plt.subplots(4, 1, figsize=(12, 10))

axs[0].plot(w_1[:500])
axs[0].set_title("Onda Original")

axs[1].plot(w_2[:4000])
axs[1].set_title("Onda Ruido")

axs[2].plot(w12[:3000])
axs[2].set_title("Onda Original + Ruidosa")

axs[3].plot(fft_freq[:len(fft_freq)//2], np.abs(fft_result)[:len(fft_result)//2])
axs[3].set_title("Frecuencias en las Ondas (FFT)")

plt.tight_layout()
plt.show()
```

> 📌 Investigar `numpy.fft.fft()`, `numpy.fft.fftfreq()` y cómo interpretar el espectro de frecuencias.

---

## Problema 2 – Filtro Complementario con Matplotlib

**Objetivo:** Graficar señales originales y filtradas usando el Filtro Complementario.

### Lo que debes hacer:
- Aplicar `Filter_Comp()` a cada señal de `aS`
- Graficar en **azul** la señal original y en **rojo** la señal filtrada
- **Explicar claramente los resultados** de las 3 gráficas (Signal 1, Signal 2, Signal 3)

### Código base proporcionado:

> ⚠️ **Este código está INCOMPLETO.** Define las señales y el filtro, pero le falta:
> 1. Declarar `aF` dentro de `Filter_Comp` (bug en el original)
> 2. Todo el bloque de graficado con Matplotlib
> 3. El valor de `nA` para llamar al filtro

```python
import numpy as np, matplotlib.pyplot as plt

FREQ_0 = 9000 ; FREQ_1 = 5000; FREQ_2 = 100  # Frecuencia 1, 2 y 3
SAMPLE = 20000 ; S_RATE = 20000.0             # Samples y Tasa de Muestreo
nMAX   = 20000

# Ondas....
aW = [
    [2*np.sin(2*np.pi * FREQ_0 * i/S_RATE) for i in range(SAMPLE)],
    [3*np.sin(2*np.pi * FREQ_1 * i/S_RATE) for i in range(SAMPLE)],
    [9*np.sin(2*np.pi * FREQ_2 * i/S_RATE) for i in range(SAMPLE)]
]

# Signals...
aS = [
    np.array(aW[0]) + np.array(aW[1]),
    np.array(aW[0]) + np.array(aW[2]),
    np.array(aW[1]) * np.array(aW[2])
]

def Filter_Comp(aV, nA):
    aF = np.zeros(nMAX)   # ⚠️ Esta línea NO está en el código original — hay que agregarla
    aF[0] = aV[0]
    for i in range(1, nMAX):
        aF[i] = nA * aV[i] + (1.0 - nA) * aF[i-1]
    return aF

# --- LO QUE DEBES AGREGAR ---

# Definir nA, aplicar el filtro a cada señal y graficar
```

**Vista del código y gráfico:**  
![Problema 2 - Filtro Complementario con Matplotlib](assets/marca2.png)

### Qué agregar (guía):
```python
nA = 0.1  # Factor del filtro complementario (entre 0 y 1)

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
```

> 📌 El parámetro `nA` controla cuánto peso tiene la muestra actual vs. el historial. Valores cercanos a 0 suavizan más la señal.

---

## Problema 3 – Control de Reproductor de Audio por Serial

**Objetivo:** Controlar remotamente Winamp o AIMP mediante comunicación serial simulada con VSPE.

### Lo que debes hacer:
- Crear una **aplicación cliente** que envíe comandos por puerto serial
- Crear una **aplicación servidor** que reciba los comandos y los ejecute en el reproductor
- Controlar al menos: `PLAY`, `STOP`, `PAUSE`, `VOLUMEN+`, `VOLUMEN-`, `NEXT`, `PREVIOUS`
- Tener al menos **10 archivos mp3/mp4** disponibles para reproducción

### Código base proporcionado:
> ❌ **No se proporcionó código base.** Debes desarrollarlo completamente desde cero.

### Estructura sugerida:

**server.py** (controla el reproductor):
```python
import win32api, win32con
import serial

# Virtual Key Codes de Windows
TECLAS = {
    'PLAY'  : 0xB3,  # VK_MEDIA_PLAY_PAUSE
    'STOP'  : 0xB2,  # VK_MEDIA_STOP
    'NEXT'  : 0xB0,  # VK_MEDIA_NEXT_TRACK
    'PREV'  : 0xB1,  # VK_MEDIA_PREV_TRACK
    'VOL+'  : 0xAF,  # VK_VOLUME_UP
    'VOL-'  : 0xAE,  # VK_VOLUME_DOWN
    'PAUSE' : 0xB3,  # VK_MEDIA_PLAY_PAUSE
}

def presionar_tecla(vk_code):
    win32api.keybd_event(vk_code, 0, 0, 0)
    win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)

ser = serial.Serial('COM1', 9600)  # Puerto configurado en VSPE
print("Servidor esperando comandos...")
while True:
    comando = ser.readline().decode().strip()
    print(f"Comando recibido: {comando}")
    if comando in TECLAS:
        presionar_tecla(TECLAS[comando])
```

**client.py** (envía comandos):
```python
import serial

ser = serial.Serial('COM2', 9600)  # Puerto par de COM1 en VSPE
print("Comandos disponibles: PLAY / STOP / PAUSE / NEXT / PREV / VOL+ / VOL-")
while True:
    cmd = input("Ingresa comando: ").strip().upper()
    ser.write((cmd + '\n').encode())
```

> 📌 Configurar VSPE para crear un par de puertos virtuales (ej: COM1 ↔ COM2). Investigar Virtual Key Codes de Windows para Winamp/AIMP.

---

## Problema 4 – Generación de Audio con el Módulo `wave`

**Objetivo:** Generar archivos `.WAV` con señales de audio usando `wave` y `struct` de Python.

### Código base proporcionado:
> ❌ **No se proporcionó código base.** Debes desarrollarlo completamente desde cero usando `wave` y `struct`.

### Frecuencias de las notas musicales (Hz):
| Nota | Frecuencia |
|------|-----------|
| Do   | 261.63 Hz |
| Re   | 293.66 Hz |
| Mi   | 329.63 Hz |
| Fa   | 349.23 Hz |
| Sol  | 392.00 Hz |
| La   | 440.00 Hz |
| Si   | 493.88 Hz |

---

### 4.1 – Escala Do→Si, Mono, 44100 Hz
```python
import wave, struct, math

RATE     = 44100
DURATION = 1
AMP      = 32767

notas = {
    'Do': 261.63, 'Re': 293.66, 'Mi': 329.63, 'Fa': 349.23,
    'Sol': 392.00, 'La': 440.00, 'Si': 493.88
}
escala = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si']

with wave.open('escala_44100_mono.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    for nota in escala:
        freq = notas[nota]
        for i in range(RATE * DURATION):
            sample = int(AMP * math.sin(2 * math.pi * freq / RATE * i))
            wf.writeframes(struct.pack('<h', sample))
```

---

### 4.2 – Escala Si→Do, Stereo, 22050 Hz
```python
import wave, struct, math

RATE     = 22050
DURATION = 1
AMP      = 32767

notas = {
    'Do': 261.63, 'Re': 293.66, 'Mi': 329.63, 'Fa': 349.23,
    'Sol': 392.00, 'La': 440.00, 'Si': 493.88
}
escala = ['Si', 'La', 'Sol', 'Fa', 'Mi', 'Re', 'Do']

with wave.open('escala_22050_stereo.wav', 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    for nota in escala:
        freq = notas[nota]
        for i in range(RATE * DURATION):
            sample = int(AMP * math.sin(2 * math.pi * freq / RATE * i))
            wf.writeframes(struct.pack('<hh', sample, sample))  # Canal L + R
```

---

### 4.3 – Escala Do→Si, Mono, 8000 Hz
```python
import wave, struct, math

RATE     = 8000
DURATION = 1
AMP      = 32767

notas = {
    'Do': 261.63, 'Re': 293.66, 'Mi': 329.63, 'Fa': 349.23,
    'Sol': 392.00, 'La': 440.00, 'Si': 493.88
}
escala = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si']

with wave.open('escala_8000_mono.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    for nota in escala:
        freq = notas[nota]
        for i in range(RATE * DURATION):
            sample = int(AMP * math.sin(2 * math.pi * freq / RATE * i))
            wf.writeframes(struct.pack('<h', sample))
```

---

### 4.4 – Onda Compuesta Stereo, 44100 Hz, 10 segundos
```python
# y = 8000*sin(2*pi*500/RATE*i) + 8000*sin(2*pi*250/RATE*i)
import wave, struct, math

RATE     = 44100
DURATION = 10

with wave.open('onda_compuesta.wav', 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(RATE)
    for i in range(RATE * DURATION):
        sample = int(8000 * math.sin(2 * math.pi * 500.0 / RATE * i) +
                     8000 * math.sin(2 * math.pi * 250.0 / RATE * i))
        wf.writeframes(struct.pack('<hh', sample, sample))
```

---

### 4.5 – Reducir volumen al 25% (bajar 75%)
```python
import wave, struct

def reducir_volumen(entrada, salida, factor=0.25):
    with wave.open(entrada, 'r') as wf_in:
        params = wf_in.getparams()
        frames = wf_in.readframes(wf_in.getnframes())

    samples = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
    samples_reducidos = [int(s * factor) for s in samples]
    frames_nuevos = struct.pack('<' + 'h' * len(samples_reducidos), *samples_reducidos)

    with wave.open(salida, 'w') as wf_out:
        wf_out.setparams(params)
        wf_out.writeframes(frames_nuevos)

reducir_volumen('onda_compuesta.wav', 'onda_volumen_bajo.wav', factor=0.25)
```

---

### 4.6 – Limpiar canal izquierdo (silenciar)
```python
import wave, struct

def limpiar_canal_izquierdo(entrada, salida):
    with wave.open(entrada, 'r') as wf_in:
        params  = wf_in.getparams()
        nframes = wf_in.getnframes()
        frames  = wf_in.readframes(nframes)

    # Stereo: índices pares = canal L, índices impares = canal R
    samples = list(struct.unpack('<' + 'h' * (len(frames) // 2), frames))
    for i in range(0, len(samples), 2):
        samples[i] = 0  # Silenciar canal izquierdo

    frames_nuevos = struct.pack('<' + 'h' * len(samples), *samples)

    with wave.open(salida, 'w') as wf_out:
        wf_out.setparams(params)
        wf_out.writeframes(frames_nuevos)

limpiar_canal_izquierdo('onda_volumen_bajo.wav', 'onda_sin_canal_izq.wav')
```

---

### 4.7 – Análisis con Audacity
- Abrir cada archivo `.wav` generado en **Audacity**
- Usar `Analizar → Graficar espectro` para ver las frecuencias presentes
- Verificar visualmente que el canal izquierdo esté en silencio en el punto 4.6
- Comparar visualmente las formas de onda entre los distintos archivos generados

---

## Resumen: Estado de los códigos por problema

| Problema | Código proporcionado | Estado |
|----------|---------------------|--------|
| 1 – FFT  | ✅ Parcial | Falta graficar y calcular FFT |
| 2 – Filtro Complementario | ✅ Parcial | Falta declarar `aF`, definir `nA` y graficar |
| 3 – Control serial | ❌ No proporcionado | Desarrollar desde cero |
| 4 – Generación WAV | ❌ No proporcionado | Desarrollar desde cero |

---

## Tecnologías y Herramientas

| Herramienta | Uso |
|---|---|
| Python | Lenguaje principal |
| NumPy | Cálculo de FFT y manejo de arrays |
| Matplotlib | Visualización de señales |
| `wave` (stdlib) | Generación de archivos WAV |
| `struct` (stdlib) | Empaquetado de datos de audio |
| Win32Api / `pywin32` | Simulación de teclas en Windows |
| `pyserial` | Comunicación serial |
| VSPE | Simulación de puertos seriales virtuales |
| Audacity | Reproducción y análisis de audio |
| Winamp / AIMP | Reproductor de audio controlado |

## Instalación de dependencias

```bash
pip install numpy matplotlib pyserial pywin32
```

---

---

## 💡 Sugerencia: Incrustar imágenes en Markdown

Para insertar imágenes locales (por ejemplo, capturas de pantalla, ecuaciones, resultados, diagramas, etc.), debes utilizar la siguiente sintaxis de Markdown:

```markdown
![Texto alternativo descriptivo](ruta/relativa/a/la/imagen.png)
```

- Ejemplo para las imágenes provistas:
    - Para insertar la imagen del primer problema:
      ```markdown
      ![Problema 1 - FFT con NumPy](assets/marca1.png)
      ```
    - Para el segundo problema:
      ```markdown
      ![Problema 2 - Filtro Complementario con Matplotlib](assets/marca2.png)
      ```

- Se recomienda que todos los recursos gráficos estén en una carpeta como `assets/` o `img/` dentro de tu repositorio/proyecto.

- El texto alternativo **debe ser descriptivo** (útil para accesibilidad y organización).

- Si subes el repositorio a GitHub, asegúrate de que la ruta relativa y el nombre del archivo sean correctos. Si el README está en la raíz y las imágenes en `assets/`, la referencia será `assets/tuimagen.png`.

---
