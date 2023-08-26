from sympy import *

# Define the symbols used in the equation
s = symbols('s', real=False)
R, C, r = symbols('R C r', positive=True, real=True)
a0, wb = symbols('a0 wb', positive=True, real=True)

# Define the equation to be simplified
ki = -s*R*C
kni = 1 - ki

arr_a0 = 1/(1 + kni/a0)
err_polo = 1/(1 + (s*kni)/(wb*a0))

h = ki * arr_a0 * err_polo

# Simplify the equation
simplified_h = simplify(h)

# Print the original and simplified equations
print('Original equation:', h)
print('Simplified equation:', simplified_h)



-C*R*a0**2*s*wb/((a0*wb + s*(C*R*s + 1))*(C*R*s + a0 + 1))