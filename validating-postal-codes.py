# Parker Addison
# 2019.04.03


# ########################################################################### #
# Paraphrased from:
# https://www.hackerrank.com/challenges/validating-postalcode/problem
#
# A valid postal code must fulfill the following requirements:
#
# 1. It must be consist of digits in the range of 100,000 to 999,999 inclusive
# 2. It must not contain more than one *alternating repetitive digit pair*
# 
# An alternating repetitive digit pair is two of the same digit separated by
# only one digit.
# 
# Example:
# 121426 has '1' as the only alt rep digit 
# 123456 has no alt rep digits
# 552523 has '2' and '5' as alt rep digits ==> invalid postal code
#
# Create two regular expressions in order to check these two conditions.
# The following expression should return whether or not a postal code is valid:
# ```
# (
#   bool(re.match(regex_integer_in_range, P))
#   and
#   len(re.findall(regex_alternating_repetitive_digit_pair, P)) < 2
# )
# ```
# 
# Input should be read from stdin.
# Output should be a boolean.
# ########################################################################### #


# The number in range validation is simple, so I'll skip my thoughts on that.
#
# The alternating repetitive digit pair pattern is much more interesting.  The
# problem wants us to return a match for every alt rep digit pair that is found
# 
# At first I thought of this pattern:
# (\d)(?!\1)\d\1
# which matches if there is a digit followed by another digit that is not the
# captured digit (negative lookahead before the middle digit match) followed by
# the captured digit.
# 
# While this works for examples like 121343, it fails to produce two matches if
# the pairs overlap, e.g. 121314
# 
# I need some way for the regex to consume only the first digit, not all three
# digits... sounds like a job for a positive lookahead!
# 
# Very simply, I took the expression I came up with above and shoved it inside
# of a positive lookahead for matching a single digit.
# 
# I now have the following:
# (?=(\d)(?!\1)\d\1)\d
# which in English will match a digit as long as that digit is captured, is
# followed by something besides that digit, and then is followed by that digit
# again. 

# Actually I just saw the example input and output—it looks like a code of
# 110000 will fail.
# i.e. the digit in the middle can be the same as the digits around it.
#
# I don't know how I got it in my head that this wasn't a thing.  But it's an
# easy fix that actually makes the pattern even simpler!
#
# Looks like I'll end up with:
# (?=(\d)\d\1)\d


import sys
import re

class Solver:
    def __init__(self):
        """
        Reads an input from stdin.

        Produces:
        self.P := The inputted postal code to be validated
        """
        self.P = sys.stdin.read().strip()

    def solve(self, P=None):
        """
        Defines the two regex's needed to validate a postal code and returns
        whether the input is a valid postal code or not.

        Test:
        >>> s = Solver.__new__(Solver)
        >>> s.solve("abc")
        False
        >>> s.solve("012345")
        False
        >>> s.solve("123456")
        True
        >>> s.solve("121345")
        True
        >>> s.solve("121343")
        False
        >>> s.solve("121234")
        False
        >>> s.solve("121314")
        False
        >>> s.solve("110000")
        False
        """

        if P is None:
            P = self.P

        regex_integer_in_range = r"^[1-9]\d{5}$"

        # Matches a digit if there it is followed by any digit and then by
        # itself.  A positive lookahead is used so that only that first digit
        # gets consumed.
        #
        # Failure to use a lookahead will result in all involved digits being
        # consumed which in turn leads to overlapping matches not being counted
        regex_alternating_repetitive_digit_pair = r"(?=(\d)\d\1)\d"

        # Provided in the writeup.
        valid = (
          bool(re.match(regex_integer_in_range, P))
          and
          len(re.findall(regex_alternating_repetitive_digit_pair, P)) < 2
        )

        return valid

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    solver = Solver()
    solver.solve()
