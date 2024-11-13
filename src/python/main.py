#//src /python/main.py
import sys
from config import get_args
from audio_capture import start_audio_stream
from audio_capture_spl import start_audio_stream_spl

def main():
    # Obtener los argumentos desde la línea de comandos
    args, samplerate = get_args()

    # Lista para almacenar los valores de SPL calculados
    spl_values = [0]

    # Mostrar las opciones de funcionalidad
    print("Seleccione una opción:")
    print("1. Calcular T60")
    print("2. Visualizar SPL en tiempo real")

    option = input("Ingrese la opción (1 o 2): ")

    if option == "1":
        print("Opción 1 seleccionada: Calcular T60.")
        # Llamar a la función para la captura de audio y calcular T60
        start_audio_stream(device=args.device, channels=args.channels, samplerate=samplerate,
                           duration=args.duration, sample_counter=[0], max_samples=args.samples,
                           spl_values=spl_values, spl_refresh_rate=args.spl_refresh_rate)
    elif option == "2":
        print("Opción 2 seleccionada: Visualizar SPL en tiempo real.")
        # Llamar a la función para la captura de audio y visualizar SPL en tiempo real
        start_audio_stream_spl(device=args.device, channels=args.channels, samplerate=samplerate,
                                spl_values=spl_values, spl_refresh_rate=args.spl_refresh_rate)
    else:
        print("Opción no válida. Elija 1 o 2.")

if __name__ == "__main__":
    main()
