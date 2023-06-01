from scipy import signal
from .utils import Param

class Filter:
    """
    Base class for all filters
    """
    def __init__(self):
        self.num = [1.0]
        self.den = [1.0]

    def compute(self):
        pass

    def getCoeffs(self):
        self.compute()
        return [self.num, self.den]
    
    def transfer(self):
        self.compute()
        return signal.TransferFunction(self.num, self.den)

    def __mul__(self, other):
        f = Filter()
        if isinstance(other, Filter):
            other.compute()

            # Multiply two polynomials together
            n = self.__polyMult__(self.num, other.num)
            d = self.__polyMult__(self.den, other.den)
            f.den = d
            f.num = n
        else:
            # Multiply polynomial by scalar
            n = [c * other for c in self.num]
            f.num = n
        return f
        
    def __polyMult__(self, p1, p2):
        m = len(p1)
        n = len(p2)
        num = [0.0] * (m + n - 1)
        for i in range(m):
            for j in range(n):
                num[i+j] += p1[i] * p2[j]
        return num


class Gain(Filter):
    def __init__(self, gain=0.0):
        super().__init__()
        self.key = "Gain"
        self.name = "Gain"
        self.params = {
            'gain': Param(gain, 'Gain', 'dB', range=[-50.0, 50.0])
        }
        self.compute()

    def compute(self):
        gain = self.params['gain'].value
        self.num = [10**(gain/20.0)]
        self.den = [1.0]


class FOLowPass(Filter):
    def __init__(self, w0=350.0):
        super().__init__()
        self.key = "FOLowPass"
        self.name = "First Order Low Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log')
        }
        self.compute()
    
    def compute(self):
        w0 = self.params['w0'].value
        self.num = [1.0]
        self.den = [1/w0, 1]



class FOHighPass(Filter):
    def __init__(self, w0=400.0):
        super().__init__()
        self.key = "FOHighPass"
        self.name = "First Order High Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log')
        }
        self.compute()
    
    def compute(self):
        w0 = self.params['w0'].value
        self.num = [1.0, 0.0]
        self.den = [1/w0, 1]


class FOAllPass(Filter):
    def __init__(self, w0=300.0):
        super().__init__()
        self.key = "FOAllPass"
        self.name = "First Order All Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log')
        }
        self.compute()
    
    def compute(self):
        w0 = self.params['w0'].value
        self.num = [1/w0, -1.0]
        self.den = [1/w0, 1.0]


class SOLowPass(Filter):
    def __init__(self, w0=450.0, xi=0.23):
        super().__init__()
        self.key = "SOLowPass"
        self.name = "Second Order Low Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'xi': Param(xi, 'ξ', 'rad/s')
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        xi = self.params['xi'].value
        if abs(w0) <= 1e-10:
            w0 = 1e-10
        self.num = [1.0]
        self.den = [w0**(-2), (2.0 * xi) / w0, 1.0]


class SOHighPass(Filter):
    def __init__(self, w0=500.0, xi=0.23):
        super().__init__()
        self.key = "SOHighPass"
        self.name = "Second Order High Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'xi': Param(xi, 'ξ', 'rad/s')
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        xi = self.params['xi'].value
        if abs(w0) <= 1e-10:
            w0 = 1e-10
        self.num = [1.0, 0.0, 0.0]
        self.den = [w0**(-2), (2.0 * xi) / w0, 1.0]


class SOAllPass(Filter):
    def __init__(self, w0=330.0, xi=0.23):
        super().__init__()
        self.key = "SOAllPass"
        self.name = "Second Order All Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'xi': Param(xi, 'ξ', 'rad/s')
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        xi = self.params['xi'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        self.num = [w0**(-2), (-2.0 * xi) / w0, 1.0]
        self.den = [w0**(-2), (2.0 * xi) / w0, 1.0]


class SOBandPass(Filter):
    def __init__(self, w0=500.0, xi=0.23):
        super().__init__()
        self.key = "SOBandPass"
        self.name = "Second Order Band Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'xi': Param(xi, 'ξ', 'rad/s')
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        xi = self.params['xi'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        self.num = [0.0, 1.0, 0.0]
        self.den = [w0**(-2), (2.0 * xi) / w0, 1.0]


class NotchFilter(Filter):
    def __init__(self, w0=600.0, xi=3.8):
        super().__init__()
        self.key = "Notch"
        self.name = "Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'xi': Param(xi, 'ξ', 'rad/s')
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        xi = self.params['xi'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        self.num = [w0**(-2), 0.0, 1.0]
        self.den = [w0**(-2), (2.0 * xi) / w0, 1.0]
        

class LowPassNotch(Filter):
    def __init__(self, w0=900.0, wz=1850.0, xi0=0.4, xiz=0.5):
        super().__init__()
        self.key = "LowPassNotch"
        self.name = "Low Pass Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'wz': Param(wz, 'ωz', 'rad/s', 'log'),
            'xi0': Param(xi0, 'ξ0', 'rad/s'),
            'xiz': Param(xiz, 'ξz', 'rad/s'),
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        wz = self.params['wz'].value
        xi0 = self.params['xi0'].value
        xiz = self.params['xiz'].value

        if wz <= w0:
            return

        if abs(w0) <= 1e-11:
            w0 = 1e-11
        if abs(wz) <= 5e-11:
            wz = 5e-11

        self.num = [wz**(-2), (2 * xiz) / wz, 1.0]
        self.den = [w0**(-2), (2.0 * xi0) / w0, 1.0]



class HighPassNotch(Filter):
    def __init__(self, w0=2130.0, wz=3450.0, xi0=0.4, xiz=0.5):
        super().__init__()
        self.key = "HighPassNotch"
        self.name = "High Pass Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'wz': Param(wz, 'ωz', 'rad/s', 'log'),
            'xi0': Param(xi0, 'ξ0', 'rad/s'),
            'xiz': Param(xiz, 'ξz', 'rad/s'),
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        wz = self.params['wz'].value
        xi0 = self.params['xi0'].value
        xiz = self.params['xiz'].value

        if wz >= w0:
            return

        if abs(w0) <= 5e-11:
            w0 = 5e-11
        if abs(wz) <= 1e-11:
            wz = 1e-11

        self.num = [wz**(-2), (2 * xiz) / wz, 1.0]
        self.den = [w0**(-2), (2.0 * xi0) / w0, 1.0]