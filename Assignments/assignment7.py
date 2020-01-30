# 1) Create a Food class with a “name” and a “kind” attribute as well as a “describe()” method (which prints “name” and “kind” in a sentence).

class Food:

    name = 'a'
    kind = 'b'
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __repr__(self):
        return(self.name,self.kind)

    def describe(self):
        print('Food is {} and is of kind {}'.format(self.name, self.kind))

# 2) Try turning describe() from an instance method into a class and a static method. Change it back to an instance method thereafter.
'''
    @staticmethod                                                       # Will fail because it uses attributes
    def describe(name,kind):
        print('Food is {} and is of kind {}'.format(name, kind))

    @classmethod
    def describe(cls):
        print('Food is {} and is of kind {}'.format(cls.name, cls.kind))
'''
# 3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook()” method to “Meat” and “clean()” to “Fruit”.

class Meat(Food):
    def cook(self):
        print('Cooking')

class Fruit(Food):
    def clean(self):
        print('cleaning')
# 4) Overwrite a “dunder” method to be able to print your “Food” class.




#banana = Food('Banana','Fruit')
#pork = Food('Pork', 'Meat')

#banana.describe()
#banana=Fruit('Banana', 'Fruit')
#banana.clean()