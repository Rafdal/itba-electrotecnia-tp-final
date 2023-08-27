import sympy as sp
import numpy as np

class OpAmp():
    def __init__(self, s = sp.symbols('s', real=False)) -> None:
        self.s = s
        self.k = sp.symbols('k', real=False)
        self.kni = sp.symbols('kni', real=False)
        self.a0 = sp.symbols('a0', positive=True, real=True)
        self.wb = sp.symbols('wb', positive=True, real=True)

        self.a0_val = 223000 # TL082
        self.wb_val = 2*sp.pi*15 # TL082

    def set_ki(self, ki):
        self.k = ki
        self.kni = 1 - ki
    
    def set_kni(self, kni):
        self.k = kni
        self.kni = kni

    def get_h(self):
        a = self.a0 / (1 + self.s / self.wb)
        err_a = 1/(1 + self.kni/a)
        self.h = sp.simplify(self.k * err_a)
        return self.h
    
    def pretty_print(self):
        num = sp.numer(self.get_h())
        den = sp.denom(self.get_h())
        poly = sp.Poly(den, self.s)
        den = poly.expr
        indep_term = poly.TC()

        coeffs = poly.coeffs()
        for i in range(0, poly.length()):
            coeffs[i] = sp.simplify(sp.simplify(coeffs[i])/sp.simplify(indep_term))

        poly = sp.Poly.from_list(coeffs, s)

        print('H(s) = \n')
        sp.pretty_print( sp.simplify(num/self.wb) / (sp.simplify(indep_term/self.wb) * poly.expr), wrap_line=False)

    def eval(self, symbols, values):
        self.h = self.get_h()
        self.h = self.h.subs(symbols, values)
        self.h_func = sp.lambdify(self.s, self.h, 'numpy')
        return self.h_func


R, C, r = sp.symbols('R C r', positive=True, real=True)
s = sp.symbols('s', real=False)

# Define the equation to be simplified
k_der = -s*R*C
k_int = -1/(s*R*C)
k_der_comp = -s*R*C/(1 + s*r*C)
k_int_comp = -r/(R*(1 + s*r*C))

opamp = OpAmp(s)
opamp.set_ki(k_der)
opamp.pretty_print()