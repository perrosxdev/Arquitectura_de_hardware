#
# Explicación de cada función del código
#

## Explicación de las funciones principales

### generar_muestras
Esta función crea una lista de números que representan una onda de sonido (senoidal) para una frecuencia, duración y sample rate dados. Básicamente, simula cómo se vería la onda de una nota musical en la computadora, generando los valores que luego se guardan en el archivo de audio. Cada valor es la amplitud de la onda en un instante de tiempo.

### generar_muestras_decimacion
Esta versión hace lo mismo que la anterior (genera la onda), pero después aplica **decimación**: se queda solo con 1 de cada N valores (por ejemplo, si N=2, toma uno, salta uno, toma uno, etc). Esto reduce la cantidad de datos y puede simular una señal con menos "detalle" o menor tasa de muestreo. Es útil para experimentar cómo afecta la decimación al sonido.

### escribir_mono
Toma una lista de muestras y la guarda en un archivo WAV mono (un solo canal). Convierte cada número a bytes usando `struct.pack` y los escribe en el archivo. Así puedes escuchar la señal generada en cualquier reproductor.

### escribir_estereo
Hace lo mismo que `escribir_mono`, pero para dos canales (izquierdo y derecho). Junta los valores de ambos canales y los guarda intercalados en el archivo WAV estéreo.

### leer_estereo
Abre un archivo WAV estéreo y separa los valores de los canales izquierdo y derecho, devolviéndolos como dos listas. Usa `struct.unpack` para convertir los bytes del archivo de vuelta a números. Esto permite modificar o analizar el audio ya guardado.

### main
Es la función principal que ejecuta todos los pasos del problema: genera las escalas, la onda compuesta, baja el volumen y limpia el canal izquierdo, llamando a las funciones anteriores en el orden correcto.

# Explicación del Código – problema4.py

## Resumen General
Este script genera archivos de audio WAV con diferentes escalas musicales, sample rates y configuraciones mono/estéreo, además de manipular señales para tareas como reducción de volumen y limpieza de canales usando técnicas de procesamiento digital de señales (FFT y filtros digitales).

---

## Explicación Paso a Paso

### 1. Generación de Notas Musicales
- **Fórmula de Frecuencias:**
  - Se usa la fórmula $f = 440 \cdot 2^{n/12}$ para calcular la frecuencia de cada nota, donde $n$ es el número de semitonos respecto a La4 (440 Hz).
  - Esto permite obtener frecuencias precisas para cualquier nota musical.
- **Función `tone`:**
  - Genera una onda seno para una frecuencia, duración y sample rate dados.
  - Se usa numpy para crear el arreglo de muestras.
- **Mono y Estéreo:**
  - Para mono, se genera una sola señal.
  - Para estéreo, se generan dos canales (izquierdo y derecho).

### 2. Cambio de Sample Rate
- Se generan archivos con sample rates de 44100 Hz, 22050 Hz y 8000 Hz.
- Cambiar el sample rate afecta la calidad y el tamaño del archivo de audio.

### 3. Escritura de Archivos WAV
- Se usa el módulo `wave` para crear archivos WAV.
- `struct.pack` convierte los valores numéricos a bytes en formato PCM de 16 bits.
- Se crean archivos mono y estéreo según lo requerido.

### 4. Señal Compuesta y Reducción de Volumen
- Se genera una señal estéreo de 10 segundos combinando dos frecuencias (500 Hz y 250 Hz).
- Para bajar el volumen un 75%, se multiplica la amplitud de la señal por 0.25.
  - **¿Por qué esta forma?**
    - Es la forma más directa y eficiente, ya que la amplitud determina el volumen percibido.
    - Otras formas incluyen modificar la potencia (cuadrado de la señal) o aplicar compresión dinámica, pero multiplicar la amplitud es simple y suficiente para este caso.

### 5. Limpieza del Canal Izquierdo
- **Opción simple:** Poner el canal izquierdo en cero.
- **Opción avanzada (implementada):**
  - Se aplica FFT al canal izquierdo para transformar la señal al dominio de la frecuencia.
  - Se eliminan componentes de frecuencia entre 200 y 600 Hz (puedes ajustar este rango según lo que quieras limpiar).
  - Se reconstruye la señal con IFFT.
  - Se aplica un filtro digital pasa bajas (Butterworth) para suavizar la señal y eliminar frecuencias altas residuales.
  - Finalmente, se guarda el archivo estéreo con el canal izquierdo procesado y el derecho original.

---

## Decisiones de Diseño
- **Uso de FFT:** Permite identificar y eliminar componentes de frecuencia específicas, útil para limpiar ruidos o tonos no deseados.
- **Filtro digital:** Se usa un filtro Butterworth por su respuesta suave y fácil implementación con scipy.
- **Multiplicación de amplitud para volumen:** Es eficiente y no distorsiona la señal si se mantiene dentro del rango permitido.

---

## Otras Formas de Bajar el Volumen
- **Compresión dinámica:** Ajusta el rango dinámico de la señal, útil para audio profesional.
- **Ajuste de potencia:** Modificar la energía total de la señal, pero es más complejo y menos intuitivo.
- **Atenuadores digitales:** Usar algoritmos DSP para reducir el volumen sin distorsión.
- **Razón para elegir la amplitud:** Multiplicar la amplitud es directo, rápido y suficiente para la mayoría de los casos simples.

---

## Procesamiento FFT y Filtros Digitales
- **FFT (Transformada Rápida de Fourier):**
  - Convierte la señal del dominio del tiempo al dominio de la frecuencia.
  - Permite identificar y manipular componentes de frecuencia específicas.
- **Eliminación de Componentes:**
  - Se ponen en cero las frecuencias no deseadas en el espectro.
- **IFFT (Transformada Inversa):**
  - Reconstruye la señal en el dominio del tiempo tras modificar el espectro.
- **Filtro Digital (Butterworth):**
  - Suaviza la señal y elimina frecuencias altas residuales.

---

## Conclusión
El código cumple con todos los requerimientos del problema 4, genera archivos WAV con diferentes configuraciones, manipula el volumen y aplica técnicas avanzadas de procesamiento de señales para limpiar el canal izquierdo, explicando cada paso y decisión tomada.
