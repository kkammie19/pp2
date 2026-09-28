#Write a Python program to convert degree to radian.
"""import math

degree = float(input("Input degree: "))
radian = degree * math.pi / 180
print("Output radian:", round(radian, 6))
"""

"""#Write a Python program to calculate the area of a trapezoid.
import math 

h = float(input("Hight: "))
a = float(input("Base, first value: "))
b = float(input("Base, second value: "))

area = (a + b) * h * 1/2 

print("Expected Output:", area)"""


#Write a Python program to calculate the area of regular polygon.
"""import math

n = int(input("Input number of sides: ")) 
s = float(input("Input the length of a side: "))

area = (n * s ** 2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", round(area, 2))"""


#Write a Python program to calculate the area of a parallelogram.
import math 

l = float(input("Length of base: "))
h = float(input("Height of parallelogram: "))

area = l * h

print("Expected Output: ", area)