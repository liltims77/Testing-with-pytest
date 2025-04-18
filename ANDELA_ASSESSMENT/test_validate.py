

# ---------- UNITTTESTS ----------
import unittest
from main import validate_data

class TestValidateData(unittest.TestCase):

    def test_all_valid(self):
        data = [{"id": 1, "name": "James", "age": 20, "email": "james@gmail.com"}]
        expected = {
            "missing_values": False,
            "missing_age": False,
            "invalid_email": False
        }
        self.assertEqual(validate_data(data), expected)

    def test_missing_age(self):
        data = [{"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"}]
        expected = {
            "missing_values": True,
            "missing_age": True,
            "invalid_email": False
        }
        self.assertEqual(validate_data(data), expected)

    def test_invalid_email(self):
        data = [{"id": 3, "name": "Tom", "age": 30, "email": "notanemail"}]
        expected = {
            "missing_values": False,
            "missing_age": False,
            "invalid_email": True
        }
        self.assertEqual(validate_data(data), expected)

    def test_combined(self):
        data = [
            {"id": 1, "name": "James", "age": 20, "email": "james@gmail.gil"},
            {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
            {"id": 3, "name": None, "age": 25, "email": "bademail"},
            {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
        ]
        expected = {
            "missing_values": True,
            "missing_age": True,
            "invalid_email": True
        }
        self.assertEqual(validate_data(data), expected)

if __name__ == '__main__':
    unittest.main()



# ---------- PYTESTS ----------
# def test_all_valid_pytest():
#     data = [{"id": 1, "name": "James", "age": 20, "email": "james@gmail.com"}]
#     assert validate_data(data) == {
#         "missing_values": False,
#         "missing_age": False,
#         "invalid_email": False
#     }

# def test_missing_age_pytest():
#     data = [{"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"}]
#     assert validate_data(data) == {
#         "missing_values": True,
#         "missing_age": True,
#         "invalid_email": False
#     }

# def test_invalid_email_pytest():
#     data = [{"id": 3, "name": "Tom", "age": 30, "email": "notanemail"}]
#     assert validate_data(data) == {
#         "missing_values": False,
#         "missing_age": False,
#         "invalid_email": True
#     }

# def test_combined_pytest():
#     data = [
#         {"id": 1, "name": "James", "age": 20, "email": "james@gmail.gil"},
#         {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
#         {"id": 3, "name": None, "age": 25, "email": "bademail"},
#         {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
#     ]
#     assert validate_data(data) == {
#         "missing_values": True,
#         "missing_age": True,
#         "invalid_email": True
#     }

# ---------- PYTESTS ----------
# def test_all_valid_pytest():
#     data = [{"id": 1, "name": "James", "age": 20, "email": "james@gmail.com"}]
#     assert validate_data(data) == {
#         "missing_values": False,
#         "missing_age": False,
#         "invalid_email": False
#     }

# def test_missing_age_pytest():
#     data = [{"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"}]
#     assert validate_data(data) == {
#         "missing_values": True,
#         "missing_age": True,
#         "invalid_email": False
#     }

# def test_invalid_email_pytest():
#     data = [{"id": 3, "name": "Tom", "age": 30, "email": "notanemail"}]
#     assert validate_data(data) == {
#         "missing_values": False,
#         "missing_age": False,
#         "invalid_email": True
#     }

# def test_combined_pytest():
#     data = [
#         {"id": 1, "name": "James", "age": 20, "email": "james@gmail.gil"},
#         {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
#         {"id": 3, "name": None, "age": 25, "email": "bademail"},
#         {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
#     ]
#     assert validate_data(data) == {
#         "missing_values": True,
#         "missing_age": True,
#         "invalid_email": True
#     }
