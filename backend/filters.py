import numpy as np

def notch_filter(w, w0, xi):
    s = 1j * w
    num = 1 + (s / w0)**2
    den = 1 + ((2.0 * xi * s) / w0) + (s / w0)**2
    H = num / den
    return H