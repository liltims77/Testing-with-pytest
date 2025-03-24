# filename: test_number_array.py
import pytest

from number_array import is_number_in_array, number_array

def test_valid_numbers(number_array):
    assert is_number_in_array(number_array, 1)
    assert is_number_in_array(number_array, 5)
    assert is_number_in_array(number_array, 7)
    assert is_number_in_array(number_array, 10)

def test_invalid_numbers(number_array):
    assert not is_number_in_array(number_array, 2)
    assert not is_number_in_array(number_array, 4)
    assert not is_number_in_array(number_array, 6)
    assert not is_number_in_array(number_array, 8)


# import number_array

# def test_is_number_in_array_true(number_array):
#     assert number_array.is_number_in_array([1, 5, 7, 10], 5) == True

# def test_is_number_in_array_false(number_array):
#     assert number_array.is_number_in_array([1, 5, 7, 10], 3) == False

