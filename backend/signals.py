import numpy as np

from .utils import Param

class Sinewave:
    def __init__(self, A=1.0, f=1.0, p=0.0):
        self.key = "Sinewave"
        self.name = "Sinewave"
        self.params = {
            'A': Param(A, 'Amplitude', 'V'),
            'f': Param(f, 'Frequency', 'Hz', "log", [-2.0, 5.0]),
            'p': Param(p, 'Phase', '°', range=[-180.0, 180.0])
        }

    def __call__(self, t):
        A = self.params['A'].value
        f = self.params['f'].value
        p = self.params['p'].value
        return A * np.sin(2.0 * np.pi * f * t + (p * np.pi) / 180.0)
    

class RectangularWave:
    def __init__(self, A=1.0, f=1.0, p=0.0, d=50.0, offset=0.0):
        self.key = "RectWave"
        self.name = "Rectangular Wave"
        self.params = {
            'A': Param(A, 'Amplitude', 'V'),
            'f': Param(f, 'Frequency', 'Hz', "log", [-2.0, 5.0]),
            'p': Param(p, 'Phase', '°', range=[-180.0, 180.0]),
            'd': Param(d, 'Duty Cycle', '%', range=[0.0, 100.0]),
            'o': Param(offset, 'Offset', 'V', range=[-10.0, 10.0]),
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