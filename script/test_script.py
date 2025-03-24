def some_function():
    print ("Function in test_script.py is called")

if __name__ == '__main__':
    print ("test_script.py is being tun directly")
    some_function()
else:
    print("test_script.py has been imported")
