import unittest

from mymodule import square, double, add


class TestSquare(unittest.TestCase):
    def test1(self):
        self.assertEqual(square(2), 4) # test when 2 is given as input the output is 4.
        self.assertEqual(square(3.0), 9.0) # test when 3.0 is given as input the output is 9.0.
        self.assertEqual(square(-3), 9) # test when -3 is given as input the output is not -9.


class Testdouble(unittest.TestCase):
    def test1(self):
        self.assertEqual(double(2), 4)
        self.assertEqual(double(-3.1), -6.2)
        self.assertEqual(double(0), 0)

class Testadd(unittest.TestCase):
    def test1(self):
        self.assertEqual((2 + 4), 6)
        self.assertNotEqual((0 + 0), 1)
        self.assertEqual((2.3 + 2.3), 4.6)
        self.assertEqual(('hello' + 'world'),'helloworld')
        self.assertNotEqual((-2 -2), 0)
        self.assertEqual(add(2,2), 4)



if __name__ == '__main__':
    unittest.main() 


import pytest
from mymodule import square, double, add

def test_square():
    assert square(2) == 4  # Test when 2 is given as input, the output is 4.
    assert square(3.0) == 9.0  # Test when 3.0 is given as input, the output is 9.0.
    assert square(-3) == 9  # Test when -3 is given as input, the output is not -9.

def test_double():
    assert double(2) == 4
    assert double(-3.1) == -6.2
    assert double(0) == 0

def test_add():
    assert (2 + 4) == 6
    assert (0 + 0) != 1
    assert (2.3 + 2.3) == 4.6
    assert ('hello' + 'world') == 'helloworld'
    assert (-2 - 2) != 0
    assert add(2, 2) == 4

       


