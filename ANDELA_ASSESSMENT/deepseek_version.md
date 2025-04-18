

Data Engineering Assessment Simulation
Based on your description, I'll simulate a data engineering assessment question similar to what your friend might have encountered at Andela. Here's the reconstructed problem and a solution:

Problem Statement
You're working on an e-learning platform that consolidates student data from a large JSON file. Your task is to write a Python function called validate_data that checks each student record for three types of data quality issues:

Missing Values: Any field (id, name, age, email) that contains None

Wrong Values: Specifically for age - where age is missing (None) or not a positive integer

Invalid Email: Email addresses that don't follow standard email format

Given the sample data:
data = [
    {"id": 1, "name": "James", "age": 20, "email": "james@gmail.com"},
    {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
    {"id": 3, "name": None, "age": 25, "email": "bademail"},
    {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
]




Your function should return a dictionary with these keys:

missing_values: True if any record has missing (None) values in any field

wrong_values: True if any record has invalid age values

invalid_email: True if any record has an invalid email format





Solution
import re

def validate_data(data):
    # Initialize result dictionary
    result = {
        'missing_values': False,
        'wrong_values': False,
        'invalid_email': False
    }
    
    # Regular expression for validating email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    for record in data:
        # Check for missing values (None in any field)
        if any(value is None for value in record.values()):
            result['missing_values'] = True
        
        # Check for wrong age values (None or not a positive integer)
        age = record.get('age')
        if age is None or not isinstance(age, int) or age <= 0:
            result['wrong_values'] = True
        
        # Check for invalid email format
        email = record.get('email')
        if email is None or not re.match(email_pattern, email):
            result['invalid_email'] = True
    
    return result

# Test with the sample data
sample_data = [
    {"id": 1, "name": "James", "age": 20, "email": "james@gmail.com"},
    {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
    {"id": 3, "name": None, "age": 25, "email": "bademail"},
    {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
]

print(validate_data(sample_data))
# Expected Output: {'missing_values': True, 'wrong_values': True, 'invalid_email': True}
