# 1) Import the random function and generate both a random number between 0 and 1 as well as a random number between 1 and 10.

from random import *
import datetime as dt

def gen_ran():
    return(f'{random()}{randrange(1,10)}')

# 2) Use the datetime library together with the random number to generate a random, unique value.
def date_ran():
    print(f'{dt.datetime.now()}{gen_ran()}')

date_ran()