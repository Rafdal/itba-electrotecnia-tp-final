from scipy import signal

class Filter:
    def __init__(self, num = [1.0], den = [1.0]):
        self.num = num
        self.den = den

    def compute(self):
        pass

    def getCoeffs(self):
        self.compute()
        return [self.num, self.den]
    
    def transfer(self):
        self.compute()
        return signal.TransferFunction(self.num, self.den)

    def __mul__(self, other):
        if isinstance(other, Filter):
            other.compute()

            # Multiply two polynomials together
            n = self.__polyMult__(self.num, other.num)
            d = self.__polyMult__(self.den, other.den)
            return Filter(n, d)
        else:
            # Multiply polynomial by scalar
            return Filter([c * other for c in self.num])
        
    def __polyMult__(self, p1, p2):
        m = len(p1)
        n = len(p2)
        num = [0.0] * (m + n - 1)
        for i in range(m):
            for j in range(n):
                num[i+j] += p1[i] * p2[j]
        return num
    


class NotchFilter(Filter):
    """
    Design a notch filter with the given parameters.

    Parameters
    ----------
    w0 : float
        Notch frequency.
    xi : float
        Damping factor.

    Returns
    -------
    num : ndarray
        Numerator coefficients of the filter transfer function.
    den : ndarray
        Denominator coefficients of the filter transfer function.
    """
    def __init__(self, w0, xi):
        super().__init__()
        self.w0 = w0
        self.xi = xi
        self.compute()

    def compute(self):
        if self.w0 == 0.0:
            self.w0 = 1e-15
        self.num = [self.w0**(-2), 0.0, 1.0]
        self.den = [self.w0**(-2), (2.0 * self.xi) / self.w0, 1.0]
        