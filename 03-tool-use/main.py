from decimal import Decimal, getcontext


def calculate_pi(digits=5):
    """
    Calculate the value of pi accurate to the given number of digits
    after the decimal point, using Machin's formula:

        pi/4 = 4*arctan(1/5) - arctan(1/239)

    The arctan series is evaluated using the Decimal type for
    arbitrary precision arithmetic.

    :param digits: number of digits after the decimal point to
                   compute pi to (default 5).
    :return: Decimal value of pi rounded to `digits` decimal places.
    """
    # Use extra guard digits internally to avoid rounding errors
    # accumulating in the final result.
    getcontext().prec = digits + 15

    def arctan_inverse(x):
        """
        Compute arctan(1/x) using its Taylor series expansion:
            arctan(1/x) = 1/x - 1/(3*x^3) + 1/(5*x^5) - ...
        Uses Decimal arithmetic and stops once terms become
        negligible at the working precision.
        """
        x = Decimal(x)
        total = Decimal(0)
        term = Decimal(1) / x
        power = x
        n = 1
        sign = 1

        # Continue until the term is smaller than our precision threshold
        threshold = Decimal(1).scaleb(-(digits + 12))
        while abs(term) > threshold:
            total += sign * term / n
            n += 2
            power *= x * x
            term = Decimal(1) / power
            sign *= -1

        return total

    pi = 4 * (4 * arctan_inverse(5) - arctan_inverse(239))

    # Round the result to the requested number of decimal digits.
    quantize_exp = Decimal(1).scaleb(-digits)
    return pi.quantize(quantize_exp)


def greeting():
    print("Hi there")