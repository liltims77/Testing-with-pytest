import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# pattern = r'[+-]?\d+\.\d+'

# # Test Case
# text = "The numbers are -3.14, 0.001, and +42.56."
# matches = re.findall(pattern, text)
# print(matches)  # ['-3.14', '0.001', '+42.56']


#The prefix "is_" usually indicates the function checks a condition and returns True or False. For example:
# is_even(4) → True
# is_odd(4) → False
#The name implies a yes/no check (is_).

# is not None:
# This converts the match object into a boolean value:
# If there’s a match (valid email), the return value is True.
# If no match is found (invalid email), the return value is False.
# So, the function is explicitly designed to return True or False.


#If you're unsure about what a function returns, you can always test it directly. For example:
# print(is_valid_email("test@example.com"))  # Expected output: True
# print(is_valid_email("invalid-email"))    # Expected output: False
# print(is_valid_email(""))                 # Expected output: False



