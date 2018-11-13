# Here's a problem (given to me via word of mouth):
# Given a string of length n, what is the next lexicographically ordered permutation of that string?
# Define a function that takes in a string and returns the above result.
#
# Runtime is important, try to work in linear time.

###

# Okay, so my first step is to simply understand what I need to do.
# I should be able to have the following: "aba" => "aab"

# I think this whole thing might be easier to conceptualize if I work with a string of digits.
# 121 => 112

# I'm noticing a trend.
# If possible, we want to switch the last digit with the second to last.
# But, if the digit in position I is less than digit II, then we don't want to switch.

# My first thought is that we start at the end of the string, check to find the first digit II that
# is greater than digit I, and then switch them.  If digit I is less than all digit II, then move our
# pointer of digit I to the second to last digit.  Repeat.

# Let's try out some examples and see if we can find any mistakes
#
# Increasing string
# 1234 --> 12{3}4 ==> 1243
#
# Decreasing string
# 4321 --> 43{2}[1] --> 4{3}2[1] --> {4}32[1] --> 4{3}[2]1 --> {4}3[2]1 --> {4}[3]21 ==> None
#
# Let's come up with something that will fail for the last digit, but work the second time around
# 4231 --> 42{3}[1] --> 4{2}3[1] --> {4}23[1] --> 4{2}[3]1 --> 4321
#
# That was not exhaustive by any means... but it validates my idea.
# I'll code it now and then test it on more strings.

# Not sure what I want to do with edge cases (string already at maximum)
# I'll just ignore for now--that isn't the main purpose of this challenge!

###

# Alright.  I just thought of something as I was about to finish coding the above solution.
# What if the next lex-ordered string is the result of switching the second-last and third-last digits?
# Then, what if the last digit (switch) is greater than the fourth-last digit (search)?

# Instead of looking at one switch and all searches, I might want to look at all switch and searches that are adjacent.
# Then, if that fails, I'll look at all switches and searches that are two apart.  Et cetera.
#
# Let's find an example.
#
# Using the previous method
# 1452 --> 14{5}[2] --> 1{4}5[2] --> {1}45[2] ==> 2451
#
# Using the new method
# 1452 --> 14{5}[2] --> 1{4}[5]2 ==> 1542

###

# Okay... Once I was done with that I found a new problem
# Consider the following test (failure)
# 1442 --> 14{4}[2] --> 1{4}[4]2 --> {1}[4]42 ==> 4142
#
# When what I really want is
# 1442 ==> 2441

# But... is that not the exact opposite of what I found before with needing to swap middle elements..?
#
# It guess it boils down to actually needing to compare the elements and their resulting strings...

###

# This is going back to nested loops again... but what if every time I widen the gap between switch and search
# then I also extend the search loop.
# So, the first loop would look at just last and second-last, then the next loop would look at
# last and third-last, then second-last and third-last.
#
# 1442 --> 14{4}[2] --> 1{4}4[2] --> 1{4}[4]2 --> {1}44[2] ==> 2441
#
# Does it work with our previous tests?
# 1452 --> 14{5}[2] --> 1{4}5[2] --> 1{4}[5]2 ==> 1542
#
# I think this will work.
# Still has a pretty bad runtime.

class Solver:
    def __init__(self, string: str):
        self.string = string
        self.length = len(self.string)
    
    def next_lex(self, string: str=None) -> str:
        """ Returns the next lex-ordered permutation of the solver's string. """

        if string:
            self.__init__(string)

        # Assign `switch` to the index of the last character
        # and `search` to the index of the second-to-last.
        switch = self.length - 1
        search = switch - 1

        # I'm going to look at all pairs of adjacent switch and search indices.
        # Once search checks 0, then I'll reset switch to the last index,
        # then look at all pairs of two-apart switch and search indices.

        # I'm considering an "iteration" to be a full search of all switch and search pairs
        # As the iteration increases, I'll need to set the initial search to `switch - iteration`
        # There can be a maximum of n-1 iterations
        for iteration in range(self.length):
            switch = self.length - 1
            search = switch - iteration

            while switch > search:
                if self.string[switch] > self.string[search]:
                    return self.swap_string(search, switch)

                # Otherwise, decrement switch to bring it closer to search
                switch -= 1

            # If we made it through the entire search loop without returning, then we should increase
            # our iteration count and look for the next larger-separated pairs of switch and search.

        # If we iterated completely and didn't find anything, then there's no next permutation.
        return False

    def swap_string(self, left, right):
        s = self.string
        next_string = s[:left] + s[right] + s[left+1:right] + s[left] + s[right+1:]
        return next_string

###

# Nice.  That works as planned!
# Now, let's figure out the runtime.
#
# I have worst case potential for the following comparisons to be necessary:
#
# 1 + 2 + 3 + ... + n-2 + n-1
# = (1+n-1) + (2+n-2) + ...
# = n + n + ...
#       n-1 / 2 times
# = n * (n-1 / 2) = O(n**2)

# There's gotta be a better way

###

# Well, I know that if a substring is decreasing (e.g. 54321) then there's nothing I can change about it.
# Additionally, if a substring is decreasing, then I'd want switch to be the last digit of the substring.
#
# So, maybe I can do an initial sweep of the string so that I can ignore decreasing substrings.
#
# Let's think: What am I ultimately achieving when I get a success above?
# I have found a decreasing substring, and then I'm switching the digit just before that substring with the
# first possible digit at the end of the substring (the first digit from the end that is larger than the search)
#
# So, maybe if I can identify the first decreasing substring that is closest to the end of a string, then
# I can perhaps run this as one loop.
#
# Starting from the back, I keep expanding the substring until I find a digit that is less than the one that follows it.
# Then, I assign my switch to the digit just before that substring.
# Then, I loop through the back of the substring looking for the first digit that is greater than the switch.
# 1442{0} --> 144{20} --> 14{420} --> 1{4420} --> [1]{4420} --> [1]{442[0]} --> [1]{44[2]0} ==> 24410

    def lex(self, string:str=None) -> str:

        if string:
            self.__init__(string)

        # sub_right is the index of the rightmost element in the decreasing substring
        # sub_left is the index of the leftmost element in the decreasing substring
        sub_right = self.length - 1
        sub_left = sub_right
        switch = None

        while sub_left > -1:
            if self.string[sub_left - 1] >= self.string[sub_left]:
                sub_left -= 1

            else:
                switch = sub_left - 1
                break

        if switch is None:
            return False

        for i in range(sub_left, sub_right + 1):
            if self.string[i] < self.string[switch]:
                print(self.string[i - 1], "at", i-1,"vs",self.string[switch],"at",switch)
                new_string = self.swap_string(switch, i - 1)

                # Now I just need to reverse the substring
                return new_string[:sub_left] + new_string[sub_right:sub_left-1:-1]

s = Solver("158476531")
print(s.lex())

# Awesome!  Now what's this runtime like:
#
# Worst case we have a loop of n-1 followed by another loop of n-1.
# Soooooo, this is O(n) :)

###

# After some searching I found this problem on LeetCode, https://leetcode.com/problems/next-permutation/.
# I'll check my answer versus the solution now.

# Oh!  One thing that I missed at first was what to do with my decreasing substring
# after swapping into it--I should reverse it to make it an increasing substring (sorted minimum)
# This also means that I should swap into the substring from the left instead of the right,
# otherwise I might break the monotonicity.