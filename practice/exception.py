#Write a pytest test case to check if a function divide(a, b) correctly raises a ZeroDivisionError when dividing by zero.
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

#pytest test case

import pytest

def test_divide():
    assert divide(10, 5) == 2
    assert divide(21, 7) == 3
    assert divide(1, 2) == 0.5
    assert divide(10, 5) == 5
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# Function to be tested
# def divide(a, b):
#     if b == 0:
#         raise ZeroDivisionError("division by zero")
#     return a / b

# # pytest test case
# import pytest

# def test_divide():
#     assert divide(10, 5) == 2
#     assert divide(21, 7) == 3
#     assert divide(1, 2) == 0.5
#     # Uncomment the following line to see a failing test case
#     # assert divide(10, 5) == 5  # This will fail
#     with pytest.raises(ZeroDivisionError):
#         divide(10, 0)
