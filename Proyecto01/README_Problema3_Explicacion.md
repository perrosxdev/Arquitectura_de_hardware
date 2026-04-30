# Explicación y Uso – Problema 3 (Control de Reproductor)

Este documento explica cómo funciona la solución entregada para el Problema 3: un sistema cliente/servidor que envía comandos por un puerto serial virtual y controla un reproductor de audio en Windows (AIMP/Winamp) simulando teclas multimedia.

---

## Resumen rápido
- **Cliente (`problema3_cliente.py`)**: envía cadenas de texto (comandos) al puerto COM configurado.
- **Servidor (`problema3_server.py`)**: escucha en un puerto COM, recibe comandos y ejecuta acciones simulando pulsaciones de tecla mediante `win32api.keybd_event` (si está disponible).
- **Comunicación**: se usa un par de puertos COM virtuales (por ejemplo `COM5 <-> COM6`) creados con VSPE (o herramienta similar). El cliente abre un extremo, el servidor el otro.

---

## Flujo del sistema

Cliente → Puerto COM (virtual) → Servidor → Simulación de tecla → Reproductor

- El cliente escribe líneas como `PLAY`, `STOP`, `VOL+`, etc., terminadas en salto de línea.
- El servidor lee líneas del puerto, las decodifica y llama a `handle_command(cmd)`, que convierte el texto en una tecla virtual (VK) y llama a `press_vk()`.

---

## ¿Qué hace cada archivo?

- `problema3_cliente.py`
  - Función principal: `send_command(port, cmd, baud=9600)`.
  - Abre el puerto COM (con `pyserial`) y envía el comando seguido de `\n`.
  - Mensaje en consola: `Enviado "{cmd}" a {port}` o un error si no puede abrir el puerto.

- `problema3_server.py`
  - Define códigos virtual-key (`VK`) para las acciones multimedia (PLAY/STOP/NEXT/PREV/VOL_UP/VOL_DOWN).
  - `run_server(port, baud=9600)`: abre el puerto en modo lectura y entra en bucle leyendo líneas con `readline()`.
  - `handle_command(cmd)`: mapea la cadena recibida a una tecla virtual y llama a `press_vk(vk)`.
  - `press_vk(vk)`: usa `win32api.keybd_event` para simular la pulsación y liberación de la tecla multimedia. Si `win32api` no está disponible imprime una advertencia y no hace nada.

---

## Comandos soportados (texto que envía el cliente)

- `PLAY` — reproducir/pausa
- `STOP` — detener
- `NEXT` — pista siguiente
- `PREV` o `PREVIOUS` — pista anterior
- `VOL+` — subir volumen
- `VOL-` — bajar volumen

Los mapeos exactos están en el diccionario `VK` dentro de `problema3_server.py`.

---

## Requisitos y notas de configuración

- Ejecutar en Windows para que `win32api` funcione correctamente. Si `win32api` no está instalado, el servidor seguirá corriendo pero no enviará teclas.
- Instalar dependencias: `pyserial` (ya está en `requirements.txt`) y `pywin32` si quieres que la parte de simulación de teclas funcione.
- Crear puertos seriales virtuales (VSPE o com0com). Ejemplo recomendado: `COM5 <-> COM6`.

---

## Instrucciones de uso (rápidas)

1. Crear par de puertos virtuales (ej. `COM5` y `COM6`).
2. Iniciar el reproductor (AIMP o Winamp) en el sistema.
3. Iniciar el servidor (en la máquina que controla el reproductor):

```bash
python src/problema3_server.py --port COM5
```

4. Enviar un comando desde el cliente (puede ser otra máquina / proceso que tenga acceso al puerto opuesto):

```bash
python src/problema3_cliente.py --port COM6 PLAY
```

5. Observa en la consola del servidor: `Recibido comando: PLAY` y la acción aplicada al reproductor.

Nota: la GUI incluida (`src/gui.py`) ya lanza el servidor en un hilo y usa `problema3_cliente.send_command` para enviar comandos desde botones.

---

## Ejemplo de salida esperada

- En el cliente:

```
Enviado "PLAY" a COM6
```

- En el servidor (con `win32api` disponible):

```
Iniciando servidor serial en COM5 @ 9600bps
Recibido comando: PLAY
```

Si `win32api` no está instalado verás:

```
win32api no disponible: no se enviarán teclas (ejecutar en Windows con pywin32)
```

---

## Consideraciones y posibles mejoras

- Si quieres mayor robustez, añade validación del contenido recibido y respuestas (ACK/NACK) por serial.
- Para uso real en Windows, ejecuta el servidor con permisos suficientes y asegúrate que el reproductor responde a teclas multimedia incluso si no está en primer plano (algunos reproductores requieren foco o configuración).
- Puedes implementar retransmisión, log y control por GUI/HTTP en vez de solo consola.

---

Si quieres, puedo añadir una sección con capturas de pantalla, o crear un pequeño script de prueba que simule envío de comandos en serie automáticamente (por ejemplo, un script que envía PLAY→VOL+→NEXT cada X segundos). ¿Lo agrego?
