# main.py
import re

def validate_data(data):
    # Initialize result dictionary
    missing_values = False
    missing_age = False
    invalid_email = False

    # Regular expression for validating email
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    # email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

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
if __name__ == "__main__":
    sample_data = [
        {"id": 1, "name": "James", "age": 20, "email": "james@gmail.gil"},
        {"id": 2, "name": "Lily", "age": None, "email": "lily@example.com"},
        {"id": 3, "name": None, "age": 25, "email": "bademail"},
        {"id": 4, "name": "John", "age": 22, "email": "john.doe@gmail.com"}
    ]
    print(validate_data(sample_data))

    print(validate_data(sample_data))
