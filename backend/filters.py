from scipy import signal

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
    


class Param():
    def __init__(self, value=0.0, name="", unit=""):
        self.value = value
        self.name = name
        self.unit = unit


class FOLowPass(Filter):
    def __init__(self, w0):
        super().__init__()
        self.key = "FOLowPass"
        self.name = "First Order Low Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s')
        }
        self.compute()
    
    def compute(self):
        w0 = self.params['w0'].value
        self.num = [1.0]
        self.den = [1/w0, 1]



class FOHighPass(Filter):
    def __init__(self, w0):
        super().__init__()
        self.key = "FOHighPass"
        self.name = "First Order High Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s')
        }
        self.compute()
    
    def compute(self):
        w0 = self.params['w0'].value
        self.num = [1.0, 0.0]
        self.den = [1/w0, 1]


class FOAllPass(Filter):
    def __init__(self, w0):
        super().__init__()
        self.key = "FOAllPass"
        self.name = "First Order All Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s')
        }
        self.compute()
    
    def compute(self):
        w0 = self.params['w0'].value
        self.num = [1/w0, -1.0]
        self.den = [1/w0, 1.0]


class SOLowPass(Filter):
    def __init__(self, w0, xi):
        super().__init__()
        self.key = "SOLowPass"
        self.name = "Second Order Low Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s'),
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
    def __init__(self, w0, xi):
        super().__init__()
        self.key = "SOHighPass"
        self.name = "Second Order High Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s'),
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
    def __init__(self, w0, xi):
        super().__init__()
        self.key = "SOAllPass"
        self.name = "Second Order All Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s'),
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
    def __init__(self, w0, xi):
        super().__init__()
        self.key = "SOBandPass"
        self.name = "Second Order Band Pass"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s'),
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
    def __init__(self, w0, xi):
        super().__init__()
        self.key = "Notch"
        self.name = "Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s'),
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
    def __init__(self, w0, wz, xi0, xiz):
        super().__init__()
        self.key = "LowPassNotch"
        self.name = "Low Pass Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s'),
            'wz': Param(wz, 'ωz', 'rad/s'),
            'xi0': Param(xi0, 'ξ0', 'rad/s'),
            'xiz': Param(xiz, 'ξz', 'rad/s'),
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        wz = self.params['wz'].value
        xi0 = self.params['xi0'].value
        xiz = self.params['xiz'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        if wz <= w0:
            return

        self.num = [wz**(-2), (2 * xiz) / wz, 1.0]
        self.den = [w0**(-2), (2.0 * xi0) / w0, 1.0]



class HighPassNotch(Filter):
    def __init__(self, w0, wz, xi0, xiz):
        super().__init__()
        self.key = "HighPassNotch"
        self.name = "High Pass Notch"
        self.params = {
            'w0': Param(w0, 'ω0', 'rad/s'),
            'wz': Param(wz, 'ωz', 'rad/s'),
            'xi0': Param(xi0, 'ξ0', 'rad/s'),
            'xiz': Param(xiz, 'ξz', 'rad/s'),
        }
        self.compute()

    def compute(self):
        w0 = self.params['w0'].value
        wz = self.params['wz'].value
        xi0 = self.params['xi0'].value
        xiz = self.params['xiz'].value

        if abs(w0) <= 1e-10:
            w0 = 1e-10

        if wz >= w0:
            return

        self.num = [wz**(-2), (2 * xiz) / wz, 1.0]
        self.den = [w0**(-2), (2.0 * xi0) / w0, 1.0]