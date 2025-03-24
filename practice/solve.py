import math
import os
import random
import re
import sys

def solve(meal_cost, tip_percent, tax_percent):
    tip = meal_cost * tip_percent / 100
    tax = meal_cost * tax_percent /100
    
    total_cost = meal_cost + tip + tax
    print(round(total_cost))
    
if __name__ == '__main__':
    meal_cost = float(12.0)
    tip_percent = int(20)
    tax_percent = int(8)
    
    solve(meal_cost, tip_percent, tax_percent)