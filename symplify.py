import sympy as sp

# Define the symbols used in the equation
s = sp.symbols('s', real=False)
R, C, r = sp.symbols('R C r', positive=True, real=True)
a0, wb = sp.symbols('a0 wb', positive=True, real=True)

# Define the equation to be simplified
k_der = -s*R*C
k_int = -1/(s*R*C)
k_der_comp = -s*R*C/(1 + s*r*C)
k_int_comp = -r/(R*(1 + s*r*C))

# ki = k_int_comp
# kni = 1 - ki
ki = sp.symbols('ki', real=False)
kni = sp.symbols('kni', real=False)

# err_polo = 1/(1 + (s*kni)/(wb*a0))

a = a0 / (1 + s / wb)
err_a = 1/(1 + kni/a)
h = ki * err_a

# Simplify the equation
simplified_h = sp.simplify(h)

num = sp.numer(simplified_h)
den = sp.denom(simplified_h)
poly = sp.Poly(den, s)
den = poly.expr
indep_term = poly.TC()
# print("indep_term:", indep_term)

coeffs = poly.coeffs()
# Remove the independent term for each coefficient of the polynomial, iterate over the coefficients
for i in range(0, poly.length()):
    coeffs[i] = sp.simplify(sp.simplify(coeffs[i])/sp.simplify(indep_term))

poly = sp.Poly.from_list(coeffs, s)


# print("den:", poly.expr)

# Print the original and simplified equations
print('Original equation:', h)
print('Simplified equation:', simplified_h)
print()

print('H(s) = \n')
sp.pretty_print(num / (indep_term * poly.expr), wrap_line=False)