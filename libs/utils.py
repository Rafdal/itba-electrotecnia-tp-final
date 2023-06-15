import sympy

class Param():
    def __init__(self, value=0.0, name="", unit="", scale="linear", range=[0.0, 9.0], n=100):
        self.value = value
        self.name = name
        self.unit = unit
        self.scale = scale
        self.min = range[0]
        self.max = range[1]
        self.n = n


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

    # convert sympy coefs numbers to float
    coeffs = [float(c) for c in coeffs]
    return coeffs


def searchMaxMinInRange(x, y, t0, t1, ax = None, text = None, axisFlag = "both", c='r', s=10):
    # Search for the local maximum and minimum values in the range
    # Return two lists with the point coordinates

    max_points = []
    min_points = []

    for i in range(len(x))[1:]:
        if x[i] >= t0 and x[i] <= t1:
            if i == 0:
                if y[i] > y[i+1]:
                    max_points.append((x[i], y[i]))
                elif y[i] < y[i+1]:
                    min_points.append((x[i], y[i]))
            elif i == len(x) - 1:
                if y[i] > y[i-1]:
                    max_points.append((x[i], y[i]))
                elif y[i] < y[i-1]:
                    min_points.append((x[i], y[i]))
            else:
                if y[i] > y[i-1] and y[i] > y[i+1]:
                    max_points.append((x[i], y[i]))
                elif y[i] < y[i-1] and y[i] < y[i+1]:
                    min_points.append((x[i], y[i]))

    if ax is not None:
        # Plot the maxima and minima as red and blue dots, respectively
        for point in max_points:
            ax.scatter(point[0], point[1], c=c, marker='o', s=s)
            if text is not None:
                if text == "up":
                    ax.annotate(f'({point[0]:.2f}, {point[1]:.2f})', xy=(point[0], point[1]), xytext=(5, 5), textcoords='offset points')
                else:
                    ax.annotate(f'({point[0]:.2f}, {point[1]:.2f})', xy=(point[0], point[1]), xytext=(5, -15), textcoords='offset points')
        for point in min_points:
            ax.scatter(point[0], point[1], c=c, marker='o', s=s)
            if text is not None:
                if not text == "up":
                    ax.annotate(f'({point[0]:.2f}, {point[1]:.2f})', xy=(point[0], point[1]), xytext=(5, 5), textcoords='offset points')
                else:
                    ax.annotate(f'({point[0]:.2f}, {point[1]:.2f})', xy=(point[0], point[1]), xytext=(5, -15), textcoords='offset points')

    if axisFlag == 'x':
        max_points = [point[0] for point in max_points]
        min_points = [point[0] for point in min_points]
    elif axisFlag == 'y':
        max_points = [point[1] for point in max_points]
        min_points = [point[1] for point in min_points]

    return max_points, min_points


def mean_spacing(values):
    # Sort the values in ascending order
    sorted_values = sorted(values)

    # Calculate the differences between adjacent values
    diffs = [sorted_values[i+1] - sorted_values[i] for i in range(len(sorted_values)-1)]

    # Calculate the mean spacing
    mean_spacing = sum(diffs) / len(diffs)

    return mean_spacing


""" 
import unittest

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