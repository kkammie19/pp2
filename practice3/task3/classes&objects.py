"""Create a Class
To create a class, use the keyword class:"""

#Get your own Python Server
#Create a class named MyClass, with a property named x:

class MyClass:
  x = 5

"""Create Object
Now we can use the class named MyClass to create objects:"""

#Create an object named p1, and print the value of x:

p1 = MyClass()
print(p1.x)

"""Delete Objects
You can delete objects by using the del keyword:"""

#Delete the p1 object:

del p1

"""Multiple Objects
You can create multiple objects from the same class:
"""

#Create three objects from the MyClass class:

p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)