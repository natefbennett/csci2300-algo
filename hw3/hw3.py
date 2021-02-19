#!/usr/bin/env python3

import random

Carmichael = [
    561,
    6601,
    67902031,
    8956911601,
    438253965870337,
    999987515379253441,
    1745094470986967126132341,
    844154128953833755776750022681,
    365376903642671522645639268043801,
    1334733877147062382486934807105197899496002201113849920496510541601,
    #2887148238050771212671429597130393991977609459279722700926516024197432303799152733116328983144639225941977803110929349655578418949441740933805615113979999421542416933972905423711002751042080134966731755152859226962916775325475044445856101949404200039904432116776619949629539250452698719329070373564032273701278453899126120309244841494728976885406024976768122077071687938121709811322297802059565867
]

# Modeled after DPV Figure 1.4
# Input: Two n-bit integers z and N, an integer exponent y
# Output: x**y mod N
def r_modexp(x, y, N):
    
    if y <= 0:
        return 1

    z = r_modexp(x, (y >> 1) >> 0, N) # floor(y/2)

    # check if y is even
    if (y & 1) == 0:
        return (z**2) % N
    else:
        return ((x *(z**2)) % N)


# Non-recursive version of r_modexp()
# Input: Two n-bit integers z and N, an integer exponent y
# Output: x**y mod N
def modexp(x, y, N):

    pass


# Modeled after DPV Figure 1.8
# Input: Positive integer N, positive integer K
# Output: yes/no with number of a_i that failed the test
def primality1(N, K):

    is_prime = True
    num_pass = 0

    # pick positive integers a_1, a_2, ..., a_K < N at random
    test_nums = []
    for i in range(0, K):
        test_nums.append(random.randint(1, N-1))

    for a_i in test_nums:
        
        # if pass Fermat's little theorem
        if r_modexp(a_i, N-1, N) == 1 % N:
            num_pass += 1
        else: is_prime = False
    
    return (is_prime, num_pass)


# Modeled after Miller-Rabin primality test
# Input: Positive integer N, positive integer K
# Output: yes/no with number of a_i that failed the test
def primality2(N, K):

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
        
        z = r_modexp(a_i, u, N)

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



def testRModexp():

    print('- Testing r_modexp() -')

    for i in range(5):
        x = random.randint(1,100)
        y = random.randint(1,10)
        N = random.randint(1,100)
        ans = r_modexp(x,y,N)
        print('Test: {}**{} mod {} = {} == {}'.format( x, y, N, ans, (x**y) % N ) )


def testPrimality1(K):

    print('- Testing primality1( K = {} ) -'.format( K ))
    
    # loop through all Carmichael numbers

    for i in range(len(Carmichael)):
        is_prime, num_passed = primality1(Carmichael[i], K)
        if is_prime:
            print('Carmichael[{}] likely to be Prime'.format(i))
        else:
            print('Carmichael[{}] unlikely to be Prime -> {}/{} a_i passed Fermat\'s little theorem.'.format(i, num_passed, K))


def testPrimality2(K):

    print('- Testing primality2( K = {} ) -'.format( K ))
    
    # loop through all Carmichael numbers

    for i in range(len(Carmichael)):
        is_prime, num_passed = primality2(Carmichael[i], K)
        if is_prime:
            print('Carmichael[{}] likely to be Prime'.format(i))
        else:
            print('Carmichael[{}] unlikely to be Prime -> {}/{} a_i passed Fermat\'s little theorem.'.format(i, num_passed, K))



print('\n-- Lab 3: Primality Testing --\n')

testRModexp() # sanity check
print('')

k_vals = [10, 20, 50, 100, 1000]
for k in k_vals:
    testPrimality1(k)
    print('')
    testPrimality2(k)
    print('')

