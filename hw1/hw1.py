#!/usr/bin/env python3

import time
from matplotlib import pyplot as plt

# exponential
def fib1(n):

    if n == 0:
        return 0
    if n == 1:
        return 1

    return fib1(n-1) + fib1(n-2)

# polynomial
def fib2(n):

    if n == 0:
        return 0

    mem = [0, 0] # initalize memory array

    mem[1] = 1

    for i in range(2, n):
        temp = mem[1]
        mem[1] = mem[0] + mem[1]
        mem[0] = temp

    return mem[1]

print('-- Fibonacci Run Time Comparison --\n')

test_vals_1 = [1, 5, 10, 15, 20, 25, 30, 35, 40, 41, 42, 43]
test_vals_2 = [2**10, 2**12, 2**14, 2**16, 2**18, 2**19, 2**20]
test_vals_2_str = ['2^10', '2^12', '2^14', '2^16', '2^18', '2^19', '2^20']


print('Recursive Implementation - Exponential Time')

rt_vals_1 = []
for val in test_vals_1:
    start_time_1 = time.process_time()
    ans1 = fib1(val)
    rt1 = round(time.process_time() - start_time_1, 4)
    rt_vals_1.append(rt1)
    print('fib1({}) = {} | {} seconds'.format(val, ans1, round(rt1, 2)))
    
plt.plot(test_vals_1, rt_vals_1)
plt.show()

print('\nMemory Implementation - Polynomial Time')

rt_vals_2 = []
c = 0
for val in test_vals_2:
    start_time_2 = time.process_time()
    ans2 = fib2(val)
    rt2 = round(time.process_time() - start_time_2, 4)
    rt_vals_2.append(rt2)
    print('fib2({}) | {} seconds'.format(test_vals_2_str[c], round(rt2, 2)))
    c += 1
    
plt.plot(test_vals_2_str, rt_vals_2)
plt.show()
