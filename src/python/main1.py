#//src/python/main1.py
#Este main1 solo evalua el t60 con audios wav directamente
import argparse
import os
from calculate_t60 import calculate_t60_from_file

# Función principal
def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Calcular el T60 de un archivo WAV")
    parser.add_argument("audio_file", type=str, help="Ruta al archivo WAV de audio")
    args = parser.parse_args()

    # Verificar si el archivo existe
    if not os.path.exists(args.audio_file):
        print(f"Error: El archivo '{args.audio_file}' no existe.")
        return

    # Llamar a la función para calcular el T60 del archivo
    t60 = calculate_t60_from_file(args.audio_file)
    if t60 is not None:
        print(f"T60 calculado: {t60:.2f} segundos")
    else:
        print("No se pudo calcular el T60.")

# Ejecutar el script si es el principal
if __name__ == "__main__":
    main()
