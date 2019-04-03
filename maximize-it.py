# Parker Addison
# 2018.04.02


# ########################################################################### #
# Paraphrased from: https://www.hackerrank.com/challenges/maximize-it/problem
#
# You are given a function f(x) = x^2, and k lists where the length of k_i is
# some positive integer n_i
#
# You have to pick one element from each list so that the value from the
# following equation is maximized:
#
# S = (f(x_1) + ... + f(x_k)) % m,  where x_i is the element chosen from the
#                                   ith list
#
# The above is subject to the following constraints:
# 1 ≤ k ≤ 7
# 1 ≤ m ≤ 1000
# 1 ≤ n_i ≤ 7
# 1 ≤ Magnitude of elements in list ≤ 10^9
#
# The input is given in the following format:
# - The first line contains 2 space separated integers, k and m
# - The next k lines each contain an integer n_i denoting the number of
#   elements in the ith list, followed by n_i space separated integers denoting
#   the elements in the list
#
# The output should be S_max
# ########################################################################### #


# Note that we will have at most 7 lists of 7 elements each
# ==> 7^7 = 823,543 possible choices if we want to brute force

# Note that (∑ x_i) % m == ∑(x_i % m) % m
#
# Since there is a large upper bound on the magnitude of a list, we may want to
# apply the modulo to all lists first to make sure we can handle the numbers.

# Let
# a := ∑ x_i
# and
# r := a % m
# thus 0 ≤ r ≤ m-1
#
# We want to maximize r
#
# This can be rewritten as
# a = km + r
# where k is some non-negative integer and r is the remainder
#
# I don't think this really helps us...

# Bottom line, we don't know anything about the numbers in the lists
# e.g. the lists aren't necessarily incrementing by one, nor necessarily
#      dependent on each other, etc
#
# There's no way to know if we should pick a number or not without looking at
# it in relation to our other choices.
#
# One exception to this is that if the square equals the modulus then we're
# essentially adding zero, so we don't need to try any combinations that
# include a zero!
#
# Additionally, if we have two squares that are half of the modulus, then we
# should only try combinations with one of them at a time.
#
# However, these special cases extend all the way to adding seven squares that
# are each one seventh of the modulus.  In the end, these special cases only
# amount to a handful of comparisons so it is unlikely we will save much time.


# For purposes of parsing and solving the problem
import sys
import itertools
# For purposes of testing the code
import io

class Solver:
    def __init__(self):
        r"""
        Reads from stdin and parses the inputs.

        Produces:
        self.k := The number of lists
        self.m := The modulus
        self.lists := A collection of the lists

        Test:
        >>> stdin = sys.stdin
        >>> def cleanup():
        ...     sys.stdin = stdin
        >>> sys.stdin = io.StringIO("2 100\n2 8 12\n1 3\n")
        >>> s = Solver()
        >>> s.k == 2
        True
        >>> s.m == 100
        True
        >>> s.lists == [[8, 12], [3]]
        True
        >>> cleanup()
        """

        stdin = sys.stdin

        # Extracting k and m from the first line of input.
        self.k, self.m = map(int, next(stdin).strip().split())

        #! IMPORTANT: We don't need the lengths of the lists for any reason, so
        #  we are just ignoring the first integer on each line after the first.
        self.lists = [
            list(map(int, line.strip().split()[1:]))
            for line in stdin
        ]


    def f(self, x):
        return x**2

    # Let X be a list where X_i is the element picked from the ith list.
    def s(self, X):
        return sum(map(self.f, X)) % self.m

    def s_post_f(self, X):
        """
        Applies the S aggregation function assuming f has already been applied.
        """
        return sum(X) % self.m


    def solve(self):
        """
        Finds the maximum value of S as defined in the problem by brute force
        checking every possible combination of elements.

        Test:
        >>> s = Solver.__new__(Solver)
        >>> s.k = 3
        >>> s.m = 1000
        >>> s.lists = [[5, 4], [7, 8, 9], [5, 7, 8, 9, 10]]
        >>> s.solve()
        206
        """
        
        # We know that (∑ x_i) % m == ∑(x_i % m) % m
        #
        # Since the magnitude of each list can be up to 1e9, we should utilize
        # this to make sure we can handle summing and applying modulo to
        # potentially large numbers.
        #
        # First we apply the function as defined in the problem, f(x) = x^2
        fx_lists = [map(self.f, lst) for lst in self.lists]
        mod_lists = [map(lambda x: x % self.m, lst) for lst in fx_lists]

        # Since we have an arbitrary number of lists ∈ [1, 7] then let's just
        # use itertools to get all of the possible combinations of elements
        # i.e. Cartesian products
        all_combinations_iter = itertools.product(*mod_lists)

        s_max = max(map(self.s_post_f, all_combinations_iter))

        return s_max

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    solver = Solver()
    print(solver.solve())