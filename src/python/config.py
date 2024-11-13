# //src / python / config.py
# config.py
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Captura y cálculo SPL")
    parser.add_argument('--device', type=int, required=True, help='ID del dispositivo de entrada')
    parser.add_argument('--samplerate', type=int, default=44100, help='Frecuencia de muestreo (Hz)')
    parser.add_argument('--channels', type=int, default=1, help='Número de canales de audio')
    parser.add_argument('--samples', type=int, default=3, help='Número de muestras a grabar')
    parser.add_argument('--duration', type=float, default=8.0, help='Duración de cada muestra (segundos)')
    parser.add_argument('--spl-refresh-rate', type=int, default=100, help='Tasa de refresco de SPL en milisegundos')

    args = parser.parse_args()
    
    return args, args.samplerate
