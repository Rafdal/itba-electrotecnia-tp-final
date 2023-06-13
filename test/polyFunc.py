
import sympy
import unittest

def get_poly_coeffs(poly_str):
    coeffs = []
    try:
        x = sympy.symbols('s')
        pol = sympy.sympify(poly_str)

        coeffs = sympy.Poly(pol, x).all_coeffs()
    except:
        raise Exception(f"Formato de polinomio \"{poly_str}\" incorrecto")

    print("VVV1", coeffs, poly_str)
    for c in coeffs:
        # check if c is a valid sympy number without constants
        if not sympy.sympify(c).is_number:
            raise Exception(f"Formato de polinomio \"{poly_str}\" incorrecto")

    return coeffs



class TestGetPolyCoeffs(unittest.TestCase):
    def test_valid_polynomial(self):
        # Test a valid polynomial
        poly_str = '3*x**3 + 2*x**2 + x + 1'
        expected_coeffs = [3, 2, 1, 1]
        coeffs = get_poly_coeffs(poly_str)
        print("VVV", expected_coeffs, coeffs)
        self.assertEqual(coeffs, expected_coeffs)

    def test_invalid_polynomial(self):
        # Test an invalid polynomial
        poly_str = '3*x**3 + 2*x**2 + x + a'
        with self.assertRaises(Exception):
            get_poly_coeffs(poly_str)

    def test_invalid_polynomial_format(self):
        # Test an invalid polynomial format
        poly_str = '3x^3 + 2x^2 + x + 1'
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

if __name__ == '__main__':
    unittest.main()