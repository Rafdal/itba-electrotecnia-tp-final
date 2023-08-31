import sympy as sp
import numpy as np
from plotTools import plotBode

class OpAmp():
    def __init__(self, s = sp.symbols('s', real=False)) -> None:
        self.s = s
        self.k = sp.symbols('k', real=False)
        self.kni = sp.symbols('kni', real=False)
        self.a0 = sp.symbols('a0', positive=True, real=True)
        self.wb = sp.symbols('wb', positive=True, real=True)

        self.a0_val = 224000 # TL082
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
    
    def pretty(self):
        num = sp.numer(self.get_h())
        den = sp.denom(self.get_h())
        poly = sp.Poly(den, self.s)
        den = poly.expr
        indep_term = poly.TC()

        coeffs = poly.coeffs()
        for i in range(0, poly.length()):
            coeffs[i] = sp.simplify(sp.simplify(coeffs[i])/sp.simplify(indep_term))

        poly = sp.Poly.from_list(coeffs, s)

        # get and print Xi
        if poly.length() == 3:
            Wo = sp.sqrt(sp.simplify(1/poly.coeffs()[0]))
            B = sp.simplify(poly.coeffs()[1])
            print("Wo = ")
            sp.pretty_print(Wo, wrap_line=False)
            print("\nB = ")
            sp.pretty_print(B, wrap_line=False)
            print("\nXi = ")
            sp.pretty_print(sp.simplify((Wo * B)/2), wrap_line=False)
            print()


        h_pretty = sp.simplify(num/self.wb) / (sp.simplify(indep_term/self.wb) * poly.expr)
        return h_pretty
    
    def pretty_print(self):
        print('H(s) = \n')
        print(sp.pretty(self.pretty(), wrap_line=False))

    # Evalua la funcion H(s) asumiendo Avol = inf
    def eval_ideal(self, symbols, values, s_vals=None):
        k = self.k
        for s, v in zip(symbols, values):
            k = k.subs(s, v)
        if s_vals is None:
            return k
        
        func = sp.lambdify(self.s, k, 'numpy')
        return func(s_vals)
    
    def eval(self, symbols, values, s_vals=None):
        self.h = self.get_h()
        # add [a0, wb] to symbols and values
        symbols = [*symbols, self.a0, self.wb]
        values = [*values, self.a0_val, self.wb_val]

        for s, v in zip(symbols, values):
            self.h = self.h.subs(s, v)
        if s_vals is None:
            return self.h
        
        func = sp.lambdify(self.s, self.h, 'numpy')
        return func(s_vals)
    
    def plot(self, f, symbols, values):
        s_val = 2*np.pi*f*1j
        h_data = opamp.eval(symbols, values, s_val)
        plotBode(h_data, f)


R, C, r = sp.symbols('R C r', positive=True, real=True)
RCr_values = [5100, 10*1e-9, 5100]

s = sp.symbols('s', real=False)

# Define the equation to be simplified
k_der = -s*R*C
k_int = -1/(s*R*C)
k_der_comp = -s*R*C/(1 + s*r*C)
k_int_comp = -r/(R*(1 + s*r*C))

k = k_der

opamp = OpAmp(s)
opamp.set_ki(k_der)

# opamp.pretty_print()

# Define a logspace vector for the frequency used with the s complex variable
f = np.logspace(-0, 7, 6000)
s_val = 2*np.pi*f*1j

h_data = opamp.eval([R, C, r], RCr_values, s_val)
h_data_id = opamp.eval_ideal([R, C, r], RCr_values, s_val)

plotBode([h_data, h_data_id], f)