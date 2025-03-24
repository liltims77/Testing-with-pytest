#Write a unittest test case for a function multiply(a, b) that multiplies two numbers.

def multiply(a, b):
    return a * b

# unti test
import unittest

class TestMultiply(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 5), -5)
        self.assertEqual(multiply(0, 100), 0)
        self.assertEqual(multiply(3, 8), 21)

if __name__ == '__main__':
    unittest.main()