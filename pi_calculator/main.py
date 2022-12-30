
from random import random

def calculate_pi(count):
    pi = 0
    inside = 0
    outside = 0
    i = 0

    while i < count:
        i = i+1
        x = random()
        y = random()

        if (x*x) + (y*y) <= 1:
            inside = inside +1
        else:
            outside = outside +1

    pi = (inside * 4) / count
    print(f'Pi is = {pi}')



if __name__ == '__main__':
    calculate_pi(10000000)


