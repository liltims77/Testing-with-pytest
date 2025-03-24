# import pytest

# from email import is_valid_email

# def test_is_valid_email():
#     assert is_valid_email("test@example.com")
#     assert not is_valid_email("test@.com")
#     assert not is_valid_email("test@com")
#     assert is_valid_email("user.name+tag+sorting@example.com")
#     assert not is_valid_email("plainaddress")

# import pytest
# from utils import is_valid_email

# def test_is_valid_email():
#     assert is_valid_email("test@example.com")
#     assert not is_valid_email("test@.com")
#     assert not is_valid_email("test@com")
#     assert is_valid_email("user.name+tag+sorting@example.com")
#     assert not is_valid_email("plainaddress")

import unittest
from utils import is_valid_email

class TestIsValidEmail(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(is_valid_email("test@example.com"))  # Expecting True for valid email

    def test_invalid_email(self):
        self.assertFalse(is_valid_email("invalid-email"))  # Expecting False for invalid email

    def test_empty_email(self):
        self.assertFalse(is_valid_email(""))  # Expecting False for empty email


