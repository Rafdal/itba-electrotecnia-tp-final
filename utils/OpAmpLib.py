import sympy as sp
import numpy as np
from plotTools import plotBode

def Lambdify(s, expr, symbols, values, s_vals=None):
    for sym, v in zip(symbols, values):
        expr = expr.subs(sym, v)

    if s_vals is None:
        return expr
    
    func = sp.lambdify(s, expr, 'numpy')
    return func(s_vals)

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

        # print LaTeX
        print(sp.latex(h_pretty))

        return h_pretty
    
    def pretty_print(self):
        print('H(s) = \n')
        print(sp.pretty(self.pretty(), wrap_line=False))

    # Evalua la funcion H(s) asumiendo Avol = inf
    def eval_ideal(self, symbols, values, s_vals=None):
        k = self.k
        
        return Lambdify(self.s, k, symbols, values, s_vals)
    


    def eval(self, symbols, values, s_vals=None):
        self.h = self.get_h()
        # add [a0, wb] to symbols and values
        symbols = [*symbols, self.a0, self.wb]
        values = [*values, self.a0_val, self.wb_val]

        return Lambdify(self.s, self.h, symbols, values, s_vals)
    
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

# opampId = OpAmp(s)
# opampId.set_ki(k_int)
opamp = OpAmp(s)
opamp.set_ki(k_int)

opamp.pretty_print()

# Define a logspace vector for the frequency used with the s complex variable
f = np.logspace(-4, 1, 6000)
s_val = 2*np.pi*f*1j

h_fun = opamp.eval([R, C, r], RCr_values)
h_data = opamp.eval([R, C, r], RCr_values, s_val)

# h_data_id = opampId.eval_ideal([R, C, r], RCr_values, s_val)

Avol = opamp.a0 / (1 + s / opamp.wb)

Z1 = R

Zi = Z1 / (1 + h_fun/Avol)

# append a0_val and wb_val to RCr_values
RCr_values = [*RCr_values, opamp.a0_val, opamp.wb_val]
Zin_d = Lambdify(s, Zi, [R, C, r, opamp.a0, opamp.wb], RCr_values, s_val)
Avol_d = Lambdify(s, Avol, [opamp.a0, opamp.wb], [opamp.a0_val, opamp.wb_val], s_val)

plotBode([Zin_d, h_data, Avol_d], f)