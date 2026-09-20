#Here we create a function named my_function that prints "Hello from a function" when called.
def my_function():
  print("Hello from a function")
my_function() 

#Here is a code that converts temperature from degrees Fahrenheit to degrees Celsius.
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

#return values
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

#the pass statement 
def my_function():
  pass