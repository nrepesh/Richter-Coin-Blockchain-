# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.

def normal(another):
    print(another('Hello'))

# 2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.
normal(lambda x: x + ' person \n')

# 3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.
def normal(another, *args):
    for arg in args:
        print(another(arg))

normal(lambda x: x + ' person', 'Hello', 'Namaste', 'Bonjour')

# 4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.
def normal(another, *args):
    for arg in args:
        print('{:^20}'.format(another(arg)))

normal(lambda x: x + ' person', 'Hello', 'Namaste', 'Bonjour')