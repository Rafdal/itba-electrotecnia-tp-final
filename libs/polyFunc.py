
import sympy
import unittest

def get_poly_coeffs(func_str):
    coeffs = [1.0]
    try:
        x = sympy.symbols('x')
        if 's' in func_str:
            x = sympy.symbols('s')
        pol = sympy.sympify(func_str)

        coeffs = sympy.Poly(pol, x).all_coeffs()
    except:
        raise Exception(f"Formato de polinomio \"{func_str}\" incorrecto")

    for c in coeffs:
        # check if c is a valid sympy number without constants
        if not sympy.sympify(c).is_number:
            raise Exception(f"Formato de polinomio \"{func_str}\" incorrecto")

    return coeffs


""" 
class TestGetPolyCoeffs(unittest.TestCase):
    def test_valid_polynomial(self):
        # Test a valid polynomial
        poly_str = '3*s**3 + 2*s**2 + s + 1'
        expected_coeffs = [3, 2, 1, 1]
        coeffs = get_poly_coeffs(poly_str)
        self.assertEqual(coeffs, expected_coeffs)

    def test_invalid_polynomial(self):
        # Test an invalid polynomial
        poly_str = '3*s**3 + 2*s**2 + s + a'
        with self.assertRaises(Exception):
            get_poly_coeffs(poly_str)

    def test_invalid_polynomial_format(self):
        # Test an invalid polynomial format
        poly_str = '3s^3 + 2s^2 + s + 1'
        with self.assertRaises(Exception):
            get_poly_coeffs(poly_str)

    def test_zero_polynomial(self):
        # Test a zero polynomial
        poly_str = '0'
        expected_coeffs = [0]
        coeffs = get_poly_coeffs(poly_str)
        self.assertEqual(coeffs, expected_coeffs)

    def test_constant_polynomial(self):
        # Test a constant polynomial
        poly_str = '5'
        expected_coeffs = [5]
        coeffs = get_poly_coeffs(poly_str)
        self.assertEqual(coeffs, expected_coeffs)

    def test_negative_polynomial(self):
        # Test a negative polynomial
        poly_str = '-s**3 + 2*s**2 - s + 1'
        expected_coeffs = [-1, 2, -1, 1]
        coeffs = get_poly_coeffs(poly_str)
        self.assertEqual(coeffs, expected_coeffs)

    def test_polynomial_with_decimals(self):
        # Test a polynomial with decimals
        poly_str = '3.5*s**3 + 2.2*s**2 + 1.1*s + 1'
        expected_coeffs = [3.5, 2.2, 1.1, 1]
        coeffs = get_poly_coeffs(poly_str)
        self.assertEqual(coeffs, expected_coeffs)

if __name__ == '__main__':
    unittest.main() """