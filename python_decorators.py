

# A decorator in Python is a function that takes another function (or method) as an
# argument and extends or modifies its "behavior" without modifying its actual code.
# Decorators allow code reuse, separation of concerns, and cleaner function definitions.

# They are commonly used for:

# Logging
# Validation
# Authorization
# Timing execution
# Caching


# Basic Structure of a Decorator
# A decorator typically follows this pattern:
def decorator_function(original_function):
    def wrapper_function():
        # Code before function execution
        original_function()
        # Code after function execution
    return wrapper_function



# 1. Creating and Using a Simple Decorator
# Let’s start with a simple example where a decorator adds a message before and after a function.

def my_decorator(func):
    def wrapper():
        print("Before calling the function")
        func()
        print("After calling the function")
    return wrapper

@my_decorator
def say_hello():
    print("Hello, World!")

say_hello()

# OUTPUT
# Before calling the function
# Hello, World!
# After calling the function

# Explanation
# my_decorator(func): This is a function that takes another function (say_hello) as input.
# Inside my_decorator, the wrapper function wraps the original function (func()).
# The wrapper function adds extra functionality before and after calling func().
# @my_decorator is a shorthand for say_hello = my_decorator(say_hello), meaning say_hello() is now replaced with wrapper().
# When calling say_hello(), the decorated function executes.





ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset veryslow -acodec aac output.mp4


tim_de_video.mp4


ffmpeg -i tim_de_video.mp4 -vcodec libx264 -crf 28 -preset veryslow -acodec aac output.mp4
