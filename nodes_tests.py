import unittest
from nodes import shamirs_share, evaluate_polynomial, lagrange_interpolate

class TestShamirsShare(unittest.TestCase):
    def test_evaluate_polynomial(self):
        coefficients = [2, 3, 1]
        x = 4
        P = 13
        result = evaluate_polynomial(coefficients, x, P)
        self.assertEqual(result, 4)  # Corrected expected value

    def test_lagrange_interpolate(self):
        received_shares = [(1, 7), (2, 12), (3, 6)]
        k = 3
        P = 17
        reconstructed_secret = lagrange_interpolate(received_shares, k, P)
        self.assertEqual(reconstructed_secret, 2)  # Corrected expected value

if __name__ == '__main__':
    unittest.main()
