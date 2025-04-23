🔍 Simulated Assessment Question
You're part of a data engineering team working for an e-learning company. 
The company collects student data in JSON format. 
The data sometimes contains missing or invalid entries. 
Your task is to write a Python function to validate the data.


You're given a list of student records in the form of dictionaries. Each record contains:
"id": integer
"name": string (can be None)
"age": integer or None
"email": string (can be invalid)


✅ Requirements for the Function validate_data(data):
The function should check the list of dictionaries and return a summary dictionary with the following keys:

"missing_values": True if any record has None in any field, else False

"missing_age": True if any record has None in the age field specifically, else False

"invalid_email": True if any record has an invalid email (use a basic regex for validation), else False



🧪 Input Example:

data = [
    {"id": 1, "name": "James", "age": 20, "email": "james@gmail.gil"},
    {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
    {"id": 3, "name": None, "age": 25, "email": "bademail"},
    {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
]


🧠 Solution in Python:
import re

def validate_data(data):
    missing_values = False
    missing_age = False
    invalid_email = False

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    for record in data:
        # Check for any None values
        if any(value is None for value in record.values()):
            missing_values = True

        # Check for missing age
        if record.get('age') is None:
            missing_age = True

        # Check for invalid email
        email = record.get('email', '')
        if not re.match(email_regex, email):
            invalid_email = True

    return {
        "missing_values": missing_values,
        "missing_age": missing_age,
        "invalid_email": invalid_email
    }

# Example usage
data = [
    {"id": 1, "name": "James", "age": 20, "email": "james@gmail.gil"},
    {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
    {"id": 3, "name": None, "age": 25, "email": "bademail"},
    {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
]

print(validate_data(data))


💡 Expected Output:
{
    'missing_values': True,
    'missing_age': True,
    'invalid_email': True
}






🔬 Unit Tests
📦 Using unittest:
import unittest

class TestValidateData(unittest.TestCase):
    def test_all_valid(self):
        data = [
            {"id": 1, "name": "James", "age": 20, "email": "james@gmail.com"}
        ]
        expected = {
            "missing_values": False,
            "missing_age": False,
            "invalid_email": False
        }
        self.assertEqual(validate_data(data), expected)

    def test_missing_age(self):
        data = [
            {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"}
        ]
        expected = {
            "missing_values": True,
            "missing_age": True,
            "invalid_email": False
        }
        self.assertEqual(validate_data(data), expected)

    def test_invalid_email(self):
        data = [
            {"id": 3, "name": "Tom", "age": 30, "email": "notanemail"}
        ]
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







🧪 Using pytest:
import pytest

def test_all_valid():
    data = [{"id": 1, "name": "James", "age": 20, "email": "james@gmail.com"}]
    assert validate_data(data) == {
        "missing_values": False,
        "missing_age": False,
        "invalid_email": False
    }

def test_missing_age():
    data = [{"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"}]
    assert validate_data(data) == {
        "missing_values": True,
        "missing_age": True,
        "invalid_email": False
    }

def test_invalid_email():
    data = [{"id": 3, "name": "Tom", "age": 30, "email": "notanemail"}]
    assert validate_data(data) == {
        "missing_values": False,
        "missing_age": False,
        "invalid_email": True
    }

def test_combined():
    data = [
        {"id": 1, "name": "James", "age": 20, "email": "james@gmail.gil"},
        {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
        {"id": 3, "name": None, "age": 25, "email": "bademail"},
        {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
    ]
    assert validate_data(data) == {
        "missing_values": True,
        "missing_age": True,
        "invalid_email": True
    }





