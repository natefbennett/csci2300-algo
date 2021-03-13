import time
import cmath
import numpy as np


# simple pretty print polynomials
def CoefficientsToPolynomialStr(coefficients):
    
    poly = ""

    for i, val in enumerate(coefficients):
        if i == 0:
            poly += '({}) '.format(val)
        elif i == 1:
            poly += '+ ({})x '.format(val)
        else:
            poly += '+ ({})x^{} '.format(val, i)
            
    return poly


# makes an list of size n random coefficients
def GeneratePolynomialCoefficients(n, type=""):

    if type == "zero":
        p = np.random.randint(1, size=n)
    else: 
        p = np.random.randint(low=1, high=10, size=n)

    return p


# alg1 from lecture 11
def PolyMultNieve(A, B):
    
    # get the number of terms and initialize result array with 0's
    d = A.size 
    C = GeneratePolynomialCoefficients((2*d)-1, type="zero")

    # fill result array C
    for i, A_val in enumerate(A):
        for j, B_val in enumerate(B):
            C[i+j] += A_val * B_val

    return C


# given an integer n 
# find a power of 2 larger than or equal to n 
def NextPowerOfTwo(n):
    
    counter = 0

    # check if n is a power of 2 already
    if n >= 0 and (n & (n - 1)) == 0:
        return n

    # shift right by 1 until n == 0
    while(n != 0):
        counter += 1
        n >>= 1

    return 1 << counter # 2**counter


# Adopted from Figure 2.9 DPV
# Input: Array a= (a_0,a_1,...,a_n-1), for n a power of 2
#              w= a primitive nth root of unity
# Output: M_n(w)a
def FFT(a, w):

    # w == 1, will not be exact
    if cmath.isclose(w, 1):
        return a

    s1 = FFT(a[::2], w**2)  # even indicies
    s2 = FFT(a[1::2], w**2) # odd indicies

    n = a.size
    r = np.array([ (0+0j) for x in range(n) ]) # initalize array of complex numbers

    for j in range(int((n/2))):
        r[j] = s1[j] + (w**j * s2[j])            # fill left
        r[j+int(n/2)] = (s1[j] - (w**j * s2[j])) # fill right
    
    return r


# using fft to speed up polynomial multiplication
def PolyMultFFT(A, B):
    
    d = A.size

    n = NextPowerOfTwo((2*d)-1)
    angle = 2. * cmath.pi/n # primitive root's angle
    w = cmath.cos(angle) + cmath.sin(angle) * 1j # primitive n-th root of unity

    # zero pad A and B
    A = np.pad(A, (0, n-d))
    B = np.pad(B, (0, n-d))    

    # evaluation
    fft_A = FFT(A, w)
    fft_B = FFT(B, w)

    # multiplication
    fft_C = fft_A * fft_B # element-wise multiplication

    # interpolation
    C = 1/n * FFT(fft_C, w**-1)

    C = C[:(2*d)-1] # ignore everything after index 2d-1

    return C


# gets rid of complex components and rounds the real components to nearest value
def CleanComplexArray(a):

    new_a = GeneratePolynomialCoefficients(a.size, "zero")

    for i, val in enumerate(a):
        new_a[i] = round(np.real(val))

    return new_a


# check results
def VerifyResults(r1, r2):
    
    if r1.size != r2.size:
        return False

    # iterate through both arrays and compare values
    for val1, val2 in zip(r1, r2):
         if not cmath.isclose(val1, val2): # will not be exact
             return False

    return True


def TestDegreeValue(d):
    
    max_d_print = 100

    print("Testing Degree Value = {}\n".format(d))

    # create polynomial coefficients
    p_A = GeneratePolynomialCoefficients(d)
    p_B = GeneratePolynomialCoefficients(d)

    # print created polynomials
    if d <= max_d_print:
        print("A = {}".format(CoefficientsToPolynomialStr(p_A)))
        print("B = {}\n".format(CoefficientsToPolynomialStr(p_B)))

    # TEST 1 ----
    # run tests for nieve polynomial multiplication
    print('Testing PolyMultNieve(A,B):')
    
    start_time = time.process_time()
    res_1 = PolyMultNieve(p_A, p_B)
    rounded_time = round(time.process_time() - start_time, 4)

    # print results
    if d <= max_d_print:
        print("The resulting polynomial is: {}".format(CoefficientsToPolynomialStr(res_1)))
    print("PolyMultNieve(A,B) takes {} seconds on d={}\n".format(rounded_time, d))

    # TEST 2 ----
    # run tests for fft based polynomial multiplication
    print('Testing PolyMultFFT(A,B):')
    
    start_time = time.process_time()
    res_2 = CleanComplexArray(PolyMultFFT(p_A, p_B))
    rounded_time = round(time.process_time() - start_time, 4)

    # print results
    if d <= max_d_print:
        print("The resulting polynomial is: {}".format(CoefficientsToPolynomialStr(res_2)))
    print("PolyMultFFT(A,B) takes {} seconds on d={}\n".format(rounded_time, d))

    # check that both polynomial multiplication functions return the same values
    if VerifyResults(res_1, res_2):
        print("The results are close enough to be equal!\n")
    else:
        print("Oops, something went wrong. The results are not equal.\n")


print('\n-- Lab 5: Multiplying Large Polynomials --\n')

# initialize test degrees and run mult functions on each
d_vals = [100, 1000, 10000]

for d in d_vals:
    TestDegreeValue(d)
