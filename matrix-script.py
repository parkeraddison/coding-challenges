# Parker Addison
# 2019.04.03


# ########################################################################### #
# Paraphrased from: https://www.hackerrank.com/challenges/matrix-script/problem
#
# Neo has a complex matrix script consisting of an N × M grid of strings.  It
# consists of alphanumeric characters, spaces, and the symbols !, @,#, $, %, &
# 
# To decode the script, Neo needs to read each column and select only the
# alphanumeric characters and connect them.  Neo reads the column from top to
# bottom and starts reading from the leftmost column.
# 
# If there are symbols or spaces between two alphanumeric characters of the 
# decoded script, then Neo replaces them with a single space ' ' for better
# readability.
# 
# Neo feels that there is no need to use 'if' conditions for decoding.
# 
# Alphanumeric characters consist of [A-Za-z0-9].
# 
# The input will consist of a line containing space separated integers N and M
# followed by N lines containing M characters each, these are the rows.
# 
# Constraints:
# N > 0
# M < 100
# 
# Sample Input:
# ```
# 7 3
# Tsi
# h%x
# i #
# sM 
# $a 
# #t%
# ir!
# ```
# 
# Sample Output:
# ```
# This is Matrix# %!
# ```
# ########################################################################### #


import sys
import re
import io

class Solver:
    def __init__(self):
        r"""
        Parses an input into N and M, and keeps the remaining lines as a matrix

        Produces:
        this.N := The number of lines in the matrix
        this.M := The number of characters per line
        this.matrix := The matrix as a list of row strings

        Test:
        >>> stdin = sys.stdin
        >>> def cleanup():
        ...     sys.stdin = stdin
        >>> sys.stdin = io.StringIO(r'''4 3
        ... wic
        ... oto
        ... wso
        ...  $l
        ... ''')
        >>> s = Solver()
        >>> s.N == 4
        True
        >>> s.M == 3
        True
        >>> s.matrix == ["wic", "oto", "wso", " $l"]
        True
        >>> cleanup()
        """

        stdin = sys.stdin

        self.N, self.M = map(int, next(stdin).split())

        self.matrix = list(map(lambda str: str.strip('\n'), stdin))

    def solve(self, matrix=None):
        r"""
        Decodes a matrix using the instructions specified by the problem and
        returns the decoded message.

        Test:
        >>> matrix = [
        ... "f5i",
        ... " &m",
        ... "p@ ",
        ... "!  ",
        ... "3l$"
        ... ]
        >>> s = Solver.__new__(Solver)
        >>> s.N = 5
        >>> s.M = 3
        >>> s.solve(matrix)
        'f p 35 lim  $'
        """

        if matrix is None:
            matrix = self.matrix

        # It'll be easiest to first read our matrix column-wise and concatenate
        # the columns into a single string.  Once we do that, decoding becomes
        # trivial.
        #
        # Admittedly it would be slightly more efficient to only pass over the
        # matrix once and decode on the spot, but we're restricted to not using
        # conditionals.

        # At first I decided to read the matrix column-wise by using a nested
        # loop going through all rows for each column.  It looked like this:
        #
        # ```
        encoded_string = ''
        for col in range(self.M):
            for row in range(self.N):
                encoded_string += matrix[row][col]
        # ```
        #
        # This solution is the most readable, so I'm continuing to use it.
        # However, a perhaps cooler way to achieve the same column-wise reading
        # of the matrix uses zip.
        #
        # If you play around with zip a bit then you can note that:
        # >>> zip(*[[1, 2], [3, 4], [5, 6]])
        # [(1, 3, 5), (2, 4, 6)]
        #
        # So, a column-wise reading of the matrix could just as easily be
        # written as:
        #
        # ```
        # encoded_string = ''.join(''.join(col) for col in zip(*matrix))
        # ```
        # where you first join the characters in the column, then you join the
        # columns together.
        #
        # Note that this is far less readable, so I stuck with my original
        # decision :) 

        # The writeup says to replace symbols or spaces *between* to alphanum
        # characters with a single space.
        
        # There is a discrepancy between what the problem defines as alphanum
        # and what regex defines as part of \w
        w = r"[A-Za-z0-9]"

        # I don't want to capture the {w} before and after the spaces/symbols,
        # so this looks like another case for lookarounds.
        decoded_string = re.sub(r"(?<=%s)[\s!@#$%%&]+(?=%s)" % (w, w), ' ', encoded_string)

        # HackerRank can use Python 3, but it doesn't use 3.6, so the format
        # strings are invalid.
        # decoded_string = re.sub(rf"(?<={w})[\s!@#$%&]+(?={w})", ' ', encoded_string)

        return decoded_string

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    solver = Solver()
    print(solver.solve())
