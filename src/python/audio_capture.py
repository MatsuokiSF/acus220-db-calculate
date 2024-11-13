import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import threading
import os
from algoritmos.calculate_spl import calculate_spl

# Función de callback para capturar audio y almacenar SPL y muestras de audio
def callback(indata, frames, time, status, spl_values, recorded_samples):
    if status:
        print(status, file=sys.stderr)
    spl = calculate_spl(indata)
    spl_values[0] = spl
    recorded_samples.append(indata.copy())  # Guarda una copia de los datos de audio

# Función para mostrar SPL en la consola
def display_spl(spl_values, spl_refresh_rate):
    while True:
        if spl_values[0] != 0:
            print(f"SPL: {spl_values[0]:.2f} dB", end="\r")
        time.sleep(spl_refresh_rate / 1000.0)

# Función para grabar audio durante un tiempo específico
def record_audio(device, channels, samplerate, duration, recorded_samples, spl_values):
    with sd.InputStream(device=device, channels=channels, samplerate=samplerate,
                        callback=lambda indata, frames, time, status: callback(indata, frames, time, status, spl_values, recorded_samples)):
        print(f"Grabando durante {duration} segundos...")
        sd.sleep(int(duration * 1000))  # Ajuste para asegurar la duración exacta en milisegundos

# Función principal para capturar audio y realizar grabaciones
def start_audio_stream(device, channels, samplerate, duration, sample_counter, max_samples, spl_values, spl_refresh_rate):
    try:
        # Asegúrate de que la carpeta "samples" exista
        output_folder = "samples"
        os.makedirs(output_folder, exist_ok=True)

        print('#' * 80)
        print("Iniciando el sistema de captura de audio")
        print('#' * 80)

        # Iniciar el hilo para mostrar el SPL
        spl_thread = threading.Thread(target=display_spl, args=(spl_values, spl_refresh_rate))
        spl_thread.daemon = True
        spl_thread.start()

        # Bucle para grabar muestras
        while sample_counter[0] < max_samples:
            input("Presiona Enter para comenzar la grabación...")

            print(f"Comenzando grabación {sample_counter[0] + 1}...")
            recorded_samples = []

            # Iniciar grabación en un hilo separado para evitar bloqueos
            record_thread = threading.Thread(target=record_audio, args=(device, channels, samplerate, duration, recorded_samples, spl_values))
            record_thread.start()
            record_thread.join()

            # Guardar archivo en la carpeta "samples"
            file_name = os.path.join(output_folder, f"sample_{sample_counter[0]}.wav")
            print(f"Guardando {file_name}")
            samples = np.concatenate(recorded_samples)  # Combina todas las muestras en un solo array
            write(file_name, int(samplerate), samples)

            sample_counter[0] += 1
            print(f"Muestra {sample_counter[0]} grabada.")

    except KeyboardInterrupt:
        print('\nMedición finalizada')
    except Exception as e:
        print(f"Error: {e}")
