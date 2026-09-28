class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def is_adult(self):
        if self.age > 18:
            return True

p1 = Person("Kamilla", 21)

print(p1.is_adult())

            
    