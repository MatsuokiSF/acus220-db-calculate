import sounddevice as sd
import time
import sys
import threading
from algoritmos.calculate_spl import calculate_spl
from kivy.clock import Clock

# Inicializar el tiempo de la última actualización
last_update_time = time.time()

# Función de callback para capturar audio y calcular el SPL
def callback(indata, frames, time_info, status, spl_values, popup_instance):
    global last_update_time
    if status:
        print(status, file=sys.stderr)
    spl = calculate_spl(indata)
    spl_values[0] = spl
    
    # Actualizar el popup solo si han pasado al menos 500 ms
    current_time = time.time()
    if (current_time - last_update_time) >= 0.5:  # 500 ms
        last_update_time = current_time
        if popup_instance:
            Clock.schedule_once(lambda dt: popup_instance.update_decibels(spl))  # Actualiza en el hilo principal

# Función para mostrar SPL en la consola con tasa de refresco de 500 ms
def display_spl(spl_values):
    while True:
        if spl_values[0] != 0:
            print(f"SPL: {spl_values[0]:.2f} dB", end="\r")
        time.sleep(0.5)  # Tasa de refresco de 500 ms

def start_audio_stream_spl(device, channels, samplerate, spl_values, spl_refresh_rate, popup_instance, stop_event):
    try:
        print('#' * 80)
        print("Iniciando el sistema de captura de audio")
        print('#' * 80)

        # Iniciar el hilo para mostrar el SPL en tiempo real
        spl_thread = threading.Thread(target=display_spl, args=(spl_values,))
        spl_thread.daemon = True
        spl_thread.start()

        # Iniciar la captura de audio indefinidamente
        with sd.InputStream(device=device, channels=channels, samplerate=samplerate,
                            callback=lambda indata, frames, time, status: callback(indata, frames, time, status, spl_values, popup_instance)):
            print("Grabando indefinidamente... Presiona Ctrl+C para detener.")
            while not stop_event.is_set():  # Continuar grabación mientras stop_event no esté activado
                sd.sleep(500)  # Mantener el flujo abierto con un refresco de 500ms

    except KeyboardInterrupt:
        print('\nMedición finalizada')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Grabación detenida.")
