#!/usr/bin/env python3

import time
import math as m
from matplotlib import pyplot as plt
from random import randint


# speed up recursive calls
class memorize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


# build data list
# d is number of digits each number has
# n is the size of the list
def makeTest(d, n):
    
    l = []
    r_start = 10**(d-1)
    r_end = (10**d)-1

    for i in range(n):
        l.append( (randint(r_start, r_end), randint(r_start, r_end)) )

    return l


# Al Khwarizmi - Quadratic
# Input: n-bit positive integers x and y
# Output: product of x and y
# will not work for negative x or y
def multiply1(x, y):

    if y == 0:
        return 0

    # find first instance of z
    if (y % 2) == 0:
        z = 0
    else:
        z = x # z holds result
    
    x = x << 1 # multiply by 2
    y = m.floor(y >> 1) # divide by two and floor

    # loop though dividing y by two
    while y >= 1:

        # y odd
        if (y % 2) != 0:
            z += x # z holds result
        
        x = x << 1
        y = m.floor(y >> 1) 

    return z

bit_mult_table = {(0,1):0, (1,0):0, (0,0):0, (1,1):1}

# Divide-and-Conquer
# Input: n-bit positive integers x and y
# Output: product of x and y
# will not work for negative x or y
@memorize #decorator
def multiply2(x, y):

    n = max(x.bit_length(), y.bit_length()) # slightly faster than max(len(bin(x)[2:]), len(bin(y)[2:]))

    if n == 1 or n == 0:
        return bit_mult_table[(x,y)]

    x_L = x >> m.ceil(n >> 1)             # x left   x >> m.floor(n / 2)
    x_R = x & (1 << (m.floor(n >> 1)))-1  # x right  x & (2**(m.floor(n / 2)))-1
    y_L = y >> m.ceil(n >> 1)             # y left   y >> m.floor(n / 2)
    y_R = y & (1 << (m.floor(n >> 1)))-1  # y right  y & (2**(m.floor(n / 2)))-1

    p_1 = multiply2(x_L, y_L)
    p_2 = multiply2(x_R, y_R)
    p_3 = multiply2(x_L + x_R, y_L + y_R)

    return (p_1 << (m.floor(n >> 1) << 1)) + ((p_3 - p_1 - p_2) << (m.floor(n >> 1))) + p_2


# run test cases on Al Khwarizmi multiplication algorithm
def runMutliplication1(l):
    
    time_vals = []

    for val in l:
        start_time = time.process_time()
        ans = multiply1(*val)
        rt = round(time.process_time() - start_time, 4)
        time_vals.append(rt)

    avg_time = sum(time_vals)/len(time_vals)
    print('Average for {} Digit Numbers: {} seconds'.format(len(str(l[0][0])), avg_time))


# run test cases on divide-and-conquer multiplication algorithm
def runMutliplication2(l):
    
    time_vals = []

    for val in l:
        start_time = time.process_time()
        ans = multiply2(*val)
        rt = round(time.process_time() - start_time, 4)
        time_vals.append(rt)

    avg_time = sum(time_vals)/len(time_vals)
    print('Average for {} Digit Numbers: {} seconds'.format(len(str(l[0][0])), avg_time))


def testCorrect(l):

    print('- Testing multiply1() -')
    for val in l:
        ans = multiply1(*val)
        print('Test: {} x {} = {}'.format( val[0], val[1], ans ))

    print('\n- Testing multiply2() -')
    for val in l:
        ans = multiply2(*val)
        print('Test: {} x {} = {}'.format( val[0], val[1], ans ))


print('\n-- Lab 2: Integer Multiplication --\n')

# initialize test data
test_vals_1 = makeTest(100, 10)
test_vals_2 = makeTest(1000, 5)
test_vals_3 = makeTest(10000, 2)
test_vals_4 = makeTest(2, 5) # test correctness on small values

testCorrect(test_vals_4)
print('')

# test Al Khwarizmi algorithm
print('Al Khwarizmi - Quadratic Time')

runMutliplication1(test_vals_1)
runMutliplication1(test_vals_2)
runMutliplication1(test_vals_3)
print('')

# test Divide-and-Conquer algorithm
print('Divide-and-Conquer')

runMutliplication2(test_vals_1)
runMutliplication2(test_vals_2)
runMutliplication2(test_vals_3)
print('')