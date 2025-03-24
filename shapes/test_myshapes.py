from  myshapes import Shape

from myshapes import Circle, Triangle, Rectangle


import pytest

# Test for circle

def test_circle_area():
    circle = Circle(radius=5)
    assert circle.area() == 78

# def test_circle_area():
#     circle = Circle(radius=4)
#     assert circle.area() == 78.5

def test_circle_area_with_zero_radius():
    circle = Circle(radius=0)
    assert circle.area() == 0

# Test case for triangle
def test_triangle_area():
    triangle = Triangle(base=4, height=5)
    assert triangle.area() == 10

def test_triangle_area_with_zero_base():
    triangle = Triangle(base=0, height=6)
    assert triangle.area() == 0

# Test case for rectangle
def test_rectangle_area():
    rectangle = Rectangle(width=3, height=7)
    assert rectangle.area() == 21

def test_rectangle_area_with_zero_height():
    rectangle = Rectangle(width=3, height=0)
    assert rectangle.area() == 0



# import unittest

# # Assuming the Circle, Triangle, and Rectangle classes are already defined
# class TestShapes(unittest.TestCase):
#     # Test cases for Circle
#     def test_circle_area(self):
#         circle = Circle(radius=5)
#         self.assertEqual(circle.area(), 78)

#     def test_circle_area_with_zero_radius(self):
#         circle = Circle(radius=0)
#         self.assertEqual(circle.area(), 0)

#     def test_circle_area_incorrect(self):
#         # Testing the commented case for a wrong expectation
#         circle = Circle(radius=4)
#         self.assertNotEqual(circle.area(), 78.5)
    
#     # Test cases for Triangle
#     def test_triangle_area(self):
#         triangle = Triangle(base=4, height=5)
#         self.assertEqual(triangle.area(), 10)

#     def test_triangle_area_with_zero_base(self):
#         triangle = Triangle(base=0, height=6)
#         self.assertEqual(triangle.area(), 0)

#     # Test cases for Rectangle
#     def test_rectangle_area(self):
#         rectangle = Rectangle(width=3, height=7)
#         self.assertEqual(rectangle.area(), 21)

#     def test_rectangle_area_with_zero_height(self):
#         rectangle = Rectangle(width=3, height=0)
#         self.assertEqual(rectangle.area(), 0)

# if __name__ == '__main__':
#     unittest.main()





