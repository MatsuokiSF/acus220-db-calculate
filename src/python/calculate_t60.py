# En src/python/calculate_t60.py

import numpy as np
import soundfile as sf
from algoritmos.t60 import revtime

def calculate_t60_from_file(file_path, fs=44100):
    try:
        # Leer el archivo de audio
        signal, _ = sf.read(file_path)
        
        # Calcular el T60 de la señal
        t60 = revtime(signal, fs)
        
        if t60 is not None:
            return t60
        else:
            print(f"Advertencia: No se pudo calcular T60 para el archivo {file_path}.")
            return None
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        return None
