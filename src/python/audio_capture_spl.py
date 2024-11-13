import sounddevice as sd
import time
import sys
import threading
from algoritmos.calculate_spl import calculate_spl

# Función de callback para capturar audio y calcular el SPL
def callback(indata, frames, time, status, spl_values):
    if status:
        print(status, file=sys.stderr)
    spl = calculate_spl(indata)
    spl_values[0] = spl

# Función para mostrar SPL en la consola
def display_spl(spl_values, spl_refresh_rate):
    while True:
        if spl_values[0] != 0:
            print(f"SPL: {spl_values[0]:.2f} dB", end="\r")
        time.sleep(spl_refresh_rate / 1000.0)

# Función principal para capturar audio y visualizar el SPL
def start_audio_stream_spl(device, channels, samplerate, spl_values, spl_refresh_rate):
    try:
        print('#' * 80)
        print("Iniciando el sistema de captura de audio")
        print('#' * 80)

        # Iniciar el hilo para mostrar el SPL en tiempo real
        spl_thread = threading.Thread(target=display_spl, args=(spl_values, spl_refresh_rate))
        spl_thread.daemon = True
        spl_thread.start()

        # Iniciar la captura de audio indefinidamente
        with sd.InputStream(device=device, channels=channels, samplerate=samplerate,
                            callback=lambda indata, frames, time, status: callback(indata, frames, time, status, spl_values)):
            print("Grabando indefinidamente... Presiona Ctrl+C para detener.")
            while True:
                sd.sleep(1000)  # Mantener el flujo abierto

    except KeyboardInterrupt:
        print('\nMedición finalizada')
    except Exception as e:
        print(f"Error: {e}")