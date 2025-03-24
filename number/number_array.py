# filename: number_array.py
import pytest

def is_number_in_array(arr, number):
    return number in arr

@pytest.fixture
def number_array():
    return [1, 5, 7, 10]


# The in keyword checks whether number exists in the list arr.
# If number is in the list, it returns True; otherwise, it returns False.

# @pytest.fixture
# What this does: This is a special decorator used in pytest. A decorator is like a label that tells Python to treat the next function (number_array) in a specific way.
# Why it's used: The @pytest.fixture decorator makes the following function (in this case, number_array) reusable as a piece of test setup. It provides predefined data for tests to use.