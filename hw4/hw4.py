#!/usr/bin/env python3

import random

# Input: Two integers a and b with a>=b>=0
# Output: gcd(a,b)
# Converted from recursive solution to solve max recursion depth exceeded for 1024-bit numbers
def Euclid(a, b):
    
    while b != 0:
        tmp = a
        a = b
        b = tmp % b

    return a


# Non-recursive version of RModExp()
# Input: Two n-bit integers z and N, an integer exponent y
# Output: x**y mod N
def ModExp(x, y, N):

    # check trivial
    if y <= 0:
        return 1
    if x <= 0:
        return 0

    z = 1 # init result z

    # loop though dividing y by two
    while y >= 1:

        # y odd
        if (y & 1) == 1:
            z = (z*x) % N # z holds result
        
        x = (x*x) % N # multiply by x and take mod N
        y = (y >> 1) >> 0 # divide by two and floor

    return z


# Modeled after Miller-Rabin primality test
# Input: Positive integer N, positive integer K
# Output: yes/no with number of a_i that failed the test
def MillerRabin(N, K=10):

    is_prime = True
    num_pass = 0

    # find u, t, such that N-1 = u * 2^t
    t, u = 0, N-1

    while (u % 2) == 0:
        t += 1
        u //= 2  # integer division, otherwise casts u to float

    # pick positive integers a_1, a_2, ..., a_K < N at random
    test_nums = []
    for i in range(0, K):
        test_nums.append(random.randint(1, N-1))

    for a_i in test_nums:
        
        z = ModExp(a_i, u, N)

        # if pass Fermat's little theorem
        if z == 1 % N:
            num_pass += 1

        else:
            one_found = False
            passed_check = False

            # repeated squaring, keep track of previous value of z,
            # find first occurrence of 1 if any
            for j in range(t):
                
                prev_z = z
                z = (z**2) % N

                # a_i passes the test iff squared value is 1 and prev value is N-1
                # else ai fails the test
                if z == 1:
                    
                    # a_i also fails the test if no 1 is encountered
                    one_found = True       

                    if prev_z == N-1:
                        passed_check = True

            if one_found and passed_check:
                num_pass += 1
            else: is_prime = False

    return (is_prime, num_pass)


# generate a random n-bit (odd) number and test if prime using MillerRabin(k=10)
# if not prime, repeat
# print the n-bit prime number with the number of trials it took
def RandomPrime(n):
    
    # find first random n-bit number
    nbitnum = random.getrandbits(n)
    prime = MillerRabin(nbitnum)[0]
    
    # repeat until prime is found
    trials = 1
    while not prime:
        nbitnum = random.getrandbits(n)
        prime = MillerRabin(nbitnum)[0]
        trials += 1

    return nbitnum, trials
    

# generate a random (odd) number between 2 to M-1 that is coprime to M
def RandomRelativePrime(M):
     
    # generate random number between 2 and M-1
    e = 2*(random.randint(2, ((M >> 1) >> 0))) + 1 # (M >> 1) >> 0 = math.floor(M/2)
    
    # test possible e coprime to M
    trials = 1
    while Euclid(e, M) != 1:
        e = 2*(random.randint(2, ((M >> 1) >> 0))) + 1
        trials += 1

    return e, trials

def RunTest(n):

    # generate p, q, and M
    p, p_trials = RandomPrime(n)
    q, q_trials = RandomPrime(n)
    M = (p-1)*(q-1)

    # find a random (odd) e coprime to M, in range 2 to M-1
    e, e_trials = RandomRelativePrime(M)
    # verify relatively prime to M, GCD(e,M)=1 via Euclid in Fig 1.5

    # print run data
    print('Testing for {}-Bit Numbers:'.format(n))
    print('p: {}, bits: {}, trials: {}'.format(p, n, p_trials))
    print('q: {}, bits: {}, trials: {}'.format(q, n, q_trials))
    print('e: {}, bits: {}, trials: {}'.format(e, n, e_trials))
    print('M: {}, GCD(e,M) = {}\n'.format(M, Euclid(e, M)))

print('\n-- Lab 4: Generating Large Primes for Cryptography --\n')

RunTest(256)
RunTest(512)
RunTest(1024)