#Create a generator that generates the squares of numbers up to some number .N
"""def sqr(N):
    for i in range(1, N + 1):
        yield i ** 2

N = int(input("Enter N: ")) 

for sq in sqr(N):
    print(sq)"""


#Write a program using generator to print the even numbers between 0 and in comma separated form where is input from console.n n
"""def numbers(n):
    for i in range (0, n + 1):
        if i % 2 == 0:
            yield i 
 
n = int(input("Enter n: ")) 
print(", ". join(map(str, numbers(n))))"""


#Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and .n
"""def function(n):
    for i in range (0, n + 1):
        if i % 3 == 0  and i % 4 == 0:
             yield i 

n = int(input("Enter n: "))             
print(", ". join(map(str, function(n))))"""


#Implement a generator called to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.squares
"""def squares(a, b):
    for i in range (a, b + 1):
        yield i ** 2

a = int(input("Enter a: "))  
b = int(input("Enter b: "))  

for sq in squares(a, b):
    print (sq) """


#Implement a generator that returns all numbers from (n) down to 0.
def gen(n):
    for i in range (n, -1, -1):
        yield i 

n = int(input("Enter n: "))  

for number in gen(n):
    print(number)