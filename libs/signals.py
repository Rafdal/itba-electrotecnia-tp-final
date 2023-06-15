import numpy as np

from .utils import Param


class Pulse:
    def __init__(self, A=1.0):
        self.key = "Pulse"
        self.name = "Pulso"
        self.params = {
            'A': Param(A, 'Amplitud', 'V'),
            't_init': Param(1.0, 'Plot Start Time', 's', range=[0.0, 1.0]),
            't_stop': Param(10.0, 'Plot Stop Time', 's', range=[0.01, 30.0]),
        }
        pass

    def __call__(self, t):
        A = self.params['A'].value
        t_init = self.params['t_init'].value
        return np.piecewise(t, [t < t_init, t >= t_init], [0.0, A])


class Sinewave:
    def __init__(self, A=1.0, f=1.0, p=0.0, offset=0.0):
        self.key = "Sinewave"
        self.name = "Senoide"
        self.params = {
            'A': Param(A, 'Amplitud', 'V'),
            'f': Param(f, 'Frequencia', 'Hz', "log", [-2.0, 5.0]),
            'p': Param(p, 'Fase', '°', range=[-180.0, 180.0]),
            'o': Param(offset, 'Offset', 'V', range=[-10.0, 10.0]),
            'n_stop': Param(10.0, 'n Períodos', 'T', range=[1.0, 30.0], n=1),
        }

    def __call__(self, t):
        A = self.params['A'].value
        f = self.params['f'].value
        p = self.params['p'].value
        o = self.params['o'].value
        return A * np.sin(2.0 * np.pi * f * t + (p * np.pi) / 180.0) + o
    

class RectangularWave:
    def __init__(self, A=1.0, f=1.0, p=0.0, d=50.0, offset=0.0):
        self.key = "RectWave"
        self.name = "Rectangular Wave"
        self.params = {
            'A': Param(A, 'Amplitud', 'V'),
            'f': Param(f, 'Frecuencia', 'Hz', "log", [-2.0, 5.0]),
            'p': Param(p, 'Fase', '°', range=[-180.0, 180.0]),
            'd': Param(d, 'Duty Cycle', '%', range=[0.0, 100.0]),
            'o': Param(offset, 'Offset', 'V', range=[-10.0, 10.0]),
            'n_stop': Param(10.0, 'n Períodos', 'T', range=[1.0, 30.0], n=1),
        }

    def __call__(self, t):
        A = self.params['A'].value  # amplitude
        f = self.params['f'].value  # frequency
        p = self.params['p'].value  # phase
        d = self.params['d'].value  # duty cycle
        o = self.params['o'].value  # offset

        d = 1.0 - (d / 100.0)

        # calculate the phase of the wave
        phase = 2.0 * np.pi * f * t + (p * np.pi) / 180.0

        # calculate the value of the wave
        value = np.where((phase % (2 * np.pi)) < (2 * np.pi * d), -A, A) + o

        return value
    

class TriangularWave:
    def __init__(self, A=1.0, f=1.0, p=0.0, offset=0.0):
        self.key = "TriWave"
        self.name = "Triangular Wave"
        self.params = {
            'A': Param(A, 'Amplitud', 'V'),
            'f': Param(f, 'Frecuencia', 'Hz', "log", [-2.0, 5.0]),
            'p': Param(p, 'Fase', '°', range=[-180.0, 180.0]),
            'o': Param(offset, 'Offset', 'V', range=[-10.0, 10.0]),
            'n_stop': Param(10.0, 'n Períodos', 'T', range=[1.0, 30.0], n=1),
        }

    def __call__(self, t):
        A = self.params['A'].value
        f = self.params['f'].value
        p = self.params['p'].value
        o = self.params['o'].value

        # calculate the phase of the wave
        phase = 2.0 * np.pi * f * t + (p * np.pi) / 180.0

        # calculate the value of the wave
        value = (2.0 * A / np.pi) * np.arcsin(np.sin(phase)) + o

        return value
    

class SawtoothWave:
    def __init__(self, A=1.0, f=1.0, p=0.0, offset=0.0):
        self.key = "SawWave"
        self.name = "Sawtooth Wave"
        self.params = {
            'A': Param(A, 'Amplitud', 'V'),
            'f': Param(f, 'Frecuencia', 'Hz', "log", [-2.0, 5.0]),
            'p': Param(p, 'Fase', '°', range=[-180.0, 180.0]),
            'o': Param(offset, 'Offset', 'V', range=[-10.0, 10.0]),
            'n_stop': Param(10.0, 'n Períodos', 'T', range=[1.0, 30.0], n=1),
        }

    def __call__(self, t):
        A = self.params['A'].value
        f = self.params['f'].value
        p = self.params['p'].value
        o = self.params['o'].value

        # calculate the phase of the wave
        phase = 2.0 * np.pi * f * t + (p * np.pi) / 180.0

        # calculate the value of the wave
        value = (2.0 * A / np.pi) * np.arctan(np.tan(phase)) + o

        return value
    

class SenoidWithNoise:
    def __init__(self, A=1.0, f=100.0, p=0.0, offset=0.0, noise=0.23, noiseFreq=10000.0):
        self.key = "SinNoise"
        self.name = "Senoide con Ruido"
        self.params = {
            'A': Param(A, 'Amplitud', 'V'),
            'f': Param(f, 'Frecuencia', 'Hz', "log", [-2.0, 5.0]),
            'p': Param(p, 'Fase', '°', range=[-180.0, 180.0]),
            'o': Param(offset, 'Offset', 'V', range=[-10.0, 10.0]),
            'n': Param(noise, 'Ruido', 'V', range=[0.0, 10.0]),
            'f_n': Param(noiseFreq, 'Frecuencia Ruido', 'Hz', "log", [-2.0, 8.0]),
            'n_stop': Param(3.0, 'n Períodos', 'T', range=[1.0, 30.0], n=1),
        }

    def __call__(self, t):
        A = self.params['A'].value
        f = self.params['f'].value
        p = self.params['p'].value
        o = self.params['o'].value
        n = self.params['n'].value
        f_n = self.params['f_n'].value

        # calculate the phase of the wave
        phase = 2.0 * np.pi * f * t + (p * np.pi) / 180.0

        # calculate the value of the wave
        value = A * np.sin(phase) + o + n * (np.sin(2.0 * np.pi * f_n * t) - 1.0)

        return value