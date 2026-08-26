import unittest
from decimal import Decimal

from main import calculate_pi


class TestCalculatePi(unittest.TestCase):

    def test_default_five_digits(self):
        """calculate_pi() with default args should return pi to 5 decimal places."""
        result = calculate_pi()
        expected = Decimal("3.14159")
        self.assertEqual(result, expected)

    def test_explicit_five_digits(self):
        """calculate_pi(5) should match the known value of pi to 5 decimals."""
        result = calculate_pi(5)
        expected = Decimal("3.14159")
        self.assertEqual(result, expected)

    def test_return_type_is_decimal(self):
        """The function should return a Decimal instance."""
        result = calculate_pi()
        self.assertIsInstance(result, Decimal)

    def test_correct_number_of_decimal_places(self):
        """The returned Decimal should have exactly `digits` digits after the point."""
        for digits in (1, 2, 3, 5, 8, 10):
            result = calculate_pi(digits)
            # exponent of the Decimal tells us how many digits are after the point
            exponent = result.as_tuple().exponent
            self.assertEqual(-exponent, digits,
                              f"Expected {digits} decimal places, got exponent {exponent}")

    def test_zero_digits(self):
        """calculate_pi(0) should round pi to the nearest whole number."""
        result = calculate_pi(0)
        self.assertEqual(result, Decimal("3"))

    def test_higher_precision(self):
        """calculate_pi(10) should match a known higher-precision value of pi."""
        result = calculate_pi(10)
        expected = Decimal("3.1415926536")
        self.assertEqual(result, expected)

    def test_string_representation(self):
        """String conversion of the result should look like a normal pi value."""
        result = calculate_pi()
        self.assertEqual(str(result), "3.14159")


if __name__ == "__main__":
    unittest.main()
