#//src / python / algoritmos / calculate_spl.py
import numpy as np

# Función de cálculo de SPL
def calculate_spl(indata):
    rms = np.sqrt(np.mean(indata**2))
    spl = 20 * np.log10(rms / 20e-6) if rms > 0 else 0
    return spl
