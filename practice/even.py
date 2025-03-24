#a pytest test case to test a function is_even(n) that checks if a number is even, using parameterized tests.

#function to test

def is_even(n):
    return n % 2 == 0

import pytest
@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, False),
    (0, True),
    (-2, True),
    (-3, False)
])
def test_is_even(n, expected):
    assert is_even(n) == expected



