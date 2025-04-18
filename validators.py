# In Python, validators are functions or methods used to check 
# if a given input meets certain conditions. 
# They are commonly used in data validation, form handling, 
# and class attributes to ensure correctness before processing. 
# Validators can be implemented in various ways, such as:

# 1.Using Functions
# 2.Using property in Classes
# 3.Using Decorators
# 4.Using Pydantic for Data Validation


# 1. Using Functions as Validators
def validate_age(age):
    if not isinstance(age, int) or age < 0:
        raise ValueError("Age must be a positive integer")
    return age

# Example Usage
try:
    print(validate_age(25))  # Valid input
    print(validate_age(-5))  # Invalid input
except ValueError as e:
    print(e)


# 2. Using property in Classes
# You can use Python’s property to enforce validation when setting attributes.
class Person:
    def __init__(self, name, age):
        self._name = name
        self.age = age  # Calls the setter method

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age must be a positive integer")
        self._age = value

# Example Usage
try:
    p = Person("Alice", 30)
    print(p.age)  # Valid
    p.age = -5    # Invalid
except ValueError as e:
    print(e)


# 3. Using Decorators for Validation
# You can use decorators to validate function arguments before execution.
def validate_positive(func):
    def wrapper(value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Value must be a positive integer")
        return func(value)
    return wrapper

@validate_positive
def square(num):
    return num * num

# Example Usage
try:
    print(square(5))  # Valid input
    print(square(-3))  # Invalid input
except ValueError as e:
    print(e)


# # 4. Using Pydantic for Data Validation
# Pydantic is a popular library for structured data validation.

# from pydantic import BaseModel, conint

# class User(BaseModel):
#     name: str
#     age: conint(gt=0)  # Age must be greater than 0

# # Example Usage
# try:
#     user = User(name="John", age=25)
#     print(user)
#     invalid_user = User(name="Jane", age=-5)  # Will raise an error
# except ValueError as e:
#     print(e)
