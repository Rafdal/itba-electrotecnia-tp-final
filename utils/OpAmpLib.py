import numpy as np
import sympy as sp

class OpAmp:
    def __init__(self, s=None):
        self.ki = sp.symbols('ki', real=False)
        self.kni = sp.symbols('kni', real=False)
        self.err_a0 = 1
        self.err_polo = 1
        self.a0_val = 1e+9
        self.wb_val = 10*2*sp.pi
        if s is None:
            self.s = sp.symbols('s', real=False)
        else:
            self.s = s
        self.a0, self.wb = sp.symbols('a0 wb', positive=True, real=True)

    def add_ki(self, ki):
        self.ki = ki
        self.kni = 1 - self.ki
        self.k = self.ki

    def add_kni(self, kni):
        self.kni = kni
        self.k = self.kni
    
    def add_err_a0(self, a0_val):
        self.err_a0 = 1 / (1 + self.kni / self.a0)
        self.a0_val = a0_val
    
    def add_err_polo(self, wb_val):
        self.err_polo = 1 / (1 + (self.s * self.kni) / (self.wb * self.a0))
        self.wb_val = wb_val
    
    def get_h(self):
        self.h = self.k * self.err_a0 * self.err_polo
        self.h = sp.simplify(self.h)
        return self.h

    def evaluate(self):
        self.h = self.get_h()
        self.h = self.h.subs(self.a0, self.a0_val).subs(self.wb, self.wb_val)
        self.h = sp.simplify(self.h)
        return self.h
    

R, C, r = sp.symbols('R C r', positive=True, real=True)
s = sp.symbols('s', real=False)

# Define the equation to be simplified
ki = -s*R*C

der = OpAmp(s) # derivador sin compensar
der.add_ki(ki)
der.add_err_a0(223000)
der.add_err_polo(2*sp.pi*15)

print(der.get_h())