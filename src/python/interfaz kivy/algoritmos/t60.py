#//src / python / algoritmos / t60.py
import numpy as np
import soundfile as sf
import sys

def cumtrapz_custom(y, dx=1.0):
    return np.cumsum(y) * dx

def revtime(signal, fs):
    # Convertir a Mono si es necesario
    if len(signal.shape) > 1:
        signal = np.mean(signal, axis=1)

    # Verificar si la señal tiene suficiente longitud
    if len(signal) < 1000:  # Si la señal es muy corta, evitar el cálculo
        print("Advertencia: La señal es demasiado corta para calcular T60.")
        return None

    # Vector de tiempo
    t = np.arange(0, len(signal)) / fs

    # Calculamos la energía en tiempo inverso usando cumtrapz_custom
    E = cumtrapz_custom(signal**2, dx=1/fs)  # Integración de la energía
    E = (E - np.min(E)) / (np.max(E) - np.min(E))  # Normalización de la energía

    # Verificamos si la energía es prácticamente constante (casi cero)
    if np.max(E) == np.min(E):
        print("Advertencia: Energía constante en la señal. No se puede calcular T60.")
        return None

    # Calculamos la energía en dBSPL
    Edb = np.where(E == 0, 0, 20 * np.log10(E))

    # Verificar si la señal tiene suficiente decaimiento
    try:
        # Encontrar índices para -5 dB y -25 dB
        idx_5db = np.where(Edb <= -5)[0][0]
        idx_25db = np.where(Edb <= -25)[0][0]
    except IndexError:
        print("Advertencia: No se encontró el decaimiento necesario para calcular el T60.")
        return None

    # Convertir los índices a tiempo en segundos
    t_5db = idx_5db / fs
    t_25db = idx_25db / fs

    # Calcular T60
    t60 = (t_25db - t_5db) * 3
    return t60
