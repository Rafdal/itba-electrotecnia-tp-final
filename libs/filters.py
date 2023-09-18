from scipy import signal
from .utils import Param

import math
import numpy as np

class Filter:
    """
    Base class for all filters
    """
    def __init__(self):
        self.num = [1.0]
        self.den = [1.0]
        self.key = "-"
        self.name = "-"
        self.params = {}
        self.callback = None

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
            'gain': Param(gain, 'Gain', 'dB', range=[-100.0, 100.0])
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
        self.num = [1/w0, 0.0]
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
            'xi': Param(xi, 'ξ', 'rad/s', range=[0.0, 10.0])
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
            'xi': Param(xi, 'ξ', 'rad/s', range=[0.0, 10.0])
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        xi = self.params['xi'].value
        if abs(w0) <= 1e-10:
            w0 = 1e-10
        self.num = [w0**(-2), 0.0, 0.0]
        self.den = [w0**(-2), (2.0 * xi) / w0, 1.0]


class SOAllPass(Filter):
    def __init__(self, w0=330.0, xi=0.23):
        super().__init__()
        self.key = "SOAllPass"
        self.name = "Second Order All Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'xi': Param(xi, 'ξ', 'rad/s', range=[0.0, 10.0])
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
    def __init__(self, w0=628.0, xi=0.5):
        super().__init__()
        self.key = "SOBandPass"
        self.name = "Second Order Band Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'xi': Param(xi, 'ξ', 'rad/s', range=[0.0, 10.0])
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        xi = self.params['xi'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        self.num = [0.0, 1.0/w0, 0.0]
        self.den = [w0**(-2), (2.0 * xi) / w0, 1.0]


class NotchFilter(Filter):
    def __init__(self, w0=600.0, xi=3.8):
        super().__init__()
        self.key = "Notch"
        self.name = "Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'xi': Param(xi, 'ξ', 'rad/s', range=[0.0, 10.0])
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        xi = self.params['xi'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        self.num = [w0**(-2), 0.0, 1.0]
        self.den = [w0**(-2), (2.0 * xi) / w0, 1.0]
        
class SecondOrdPole(Filter):
    def __init__(self, w0=600.0, Q=0.5):
        super().__init__()
        self.key = "SecondOrdPole"
        self.name = "SecondOrdPole"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'Q': Param(Q, 'Q', '-', range=[-3.0, 4.0], scale='log')
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        q = self.params['Q'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        self.num = [1.0]
        self.den = [w0**(-2), 1 / (w0*q), 1.0]

class SecondOrdZero(Filter):
    def __init__(self, w0=600.0, Q=0.5):
        super().__init__()
        self.key = "SecondOrdZero"
        self.name = "SecondOrdZero"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'Q': Param(Q, 'Q', '-', range=[-3.0, 4.0], scale='log')
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        q = self.params['Q'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        self.num = [w0**(-2), 1 / (w0*q), 1.0]
        self.den = [1.0]

class LowPassNotch(Filter):
    def __init__(self, w0=900.0, wz=1850.0, xi0=0.4, xiz=0.5):
        super().__init__()
        self.key = "LowPassNotch"
        self.name = "Low Pass Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'wz': Param(wz, 'ωz', 'rad/s', 'log'),
            'xi0': Param(xi0, 'ξ0', 'rad/s', range=[0.0, 10.0]),
            'xiz': Param(xiz, 'ξz', 'rad/s', range=[0.0, 10.0]),
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

import sympy as sp
class HighOrderLowPass(Filter):
    def __init__(self, k=2, bw=3.0, w0=0.0):
        super().__init__()
        self.key = "HighOrderLowPass"
        self.name = "High Order Low Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'k': Param(k, 'k', 'orden', range=[1, 40], n=1),
            'bw': Param(bw, 'BW', 'rad/s', 'log', range=[0, 8])
        }
        self.compute()

    def compute(self):
        k = self.params['k'].value
        bw_v = self.params['bw'].value
        w0_v = self.params['w0'].value

        if abs(bw_v) <= 1:
            bw_v = 1

        w0 = sp.symbols('w0', real=True, positive=True)
        bw = sp.symbols('bw', real=True, positive=True)
        s = sp.symbols('s', real=False)
        num = bw**int(k) + w0**int(k)
        den = (s+w0)**int(k) + bw**int(k)
        # create a polynomial, get coeffs, simplify, replace w0 and bw and get coeffs again with new values
        n_poly = sp.Poly(num, s)
        d_poly = sp.Poly(den, s)
        d_coeffs = d_poly.all_coeffs()
        n_coeffs = n_poly.all_coeffs()

        for i in range(0, len(d_coeffs)):
            d_coeffs[i] = sp.simplify(sp.simplify(d_coeffs[i]).subs({bw: bw_v, w0: w0_v}))
        for i in range(0, len(n_coeffs)):
            n_coeffs[i] = sp.simplify(sp.simplify(n_coeffs[i]).subs({bw: bw_v, w0: w0_v}))

        print('n_coeffs = ', n_coeffs[::-1])
        print('d_coeffs = ', d_coeffs[::-1])
        self.num = np.array(n_coeffs).astype(np.float64)
        self.den = np.array(d_coeffs).astype(np.float64)


class HighPassNotch(Filter):
    def __init__(self, w0=3450.0, wz=2130.0, xi0=0.4, xiz=0.5):
        super().__init__()
        self.key = "HighPassNotch"
        self.name = "High Pass Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s', 'log'),
            'wz': Param(wz, 'ωz', 'rad/s', 'log'),
            'xi0': Param(xi0, 'ξ0', 'rad/s', range=[0.0, 10.0]),
            'xiz': Param(xiz, 'ξz', 'rad/s', range=[0.0, 10.0]),
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

        self.num = [1.0, 2 * xiz * wz, wz**2]
        self.den = [1.0, 2.0 * xi0 * w0, w0**2]


from widgets.PopUpForm import PopUpForm
from libs.utils import get_poly_coeffs

class CustomFilter(Filter):
    def __init__(self, on_close=lambda: print("On Filter Close")):
        super().__init__()
        self.key = "Custom"
        self.name = "Custom Filter"
        self.popUp = PopUpForm()
        self.popUp.set_callback(self.getTexts)
        self.callback = lambda: self.popUp.show()
        self.on_close = on_close
        self.callback()

    def getTexts(self, txt1, txt2):
        self.num = get_poly_coeffs(txt1)
        self.den = get_poly_coeffs(txt2)
        self.on_close()

    def compute(self):
        pass
            