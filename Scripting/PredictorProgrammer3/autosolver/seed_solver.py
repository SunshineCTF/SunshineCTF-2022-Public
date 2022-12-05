#!/usr/local/bin/python3
from math import gcd
import random

#########################################################################################################################################################################
# Python translation of the algorithm specified by Haldir[RET], "How to crack a Linear Congruential Generator" (22nd December 2004), http://www.reteam.org/papers/e59.pdf

# "Short way for calculating the determinant of a 3*3 matrix"
def calcDet(val1, val2, val3, val4):
    return abs(val1*val3 - val1*val4 + val2*val3 - val2*val2 + val2*val4 - val3*val3)

# "Just to remove a few factors, the modulus might still
# multiplied by a small factor, like 2 or 10"
def factor(value):
    sprimes = [0x02,0x03,0x05,0x07,0x0B,0x0D,0x11,0x13,0x17,0x1D,0x1F,0x25,0x29,0x2B,0x2F,0x35]
    counter = 0
    # bugfix here: if value is 0 would otherwise loop forever
    while counter < 16 and value > 0:
        if (value % sprimes[counter] == 0):
            value = value // sprimes[counter]
        else:
            counter += 1
    return value

# "Should do the trick to calculate the different GCDs of the determinants"
def getModulus(detlist):
    return factor(gcd(*detlist))

# "Short way to solve the 2 equations"
def linsolve(val1, val2, val3, modulus):
    top = (val2-val3) % modulus
    bottom = (val1-val2) % modulus
    bottom_inv = modinv(bottom, modulus)
    retval1 = (top * bottom_inv) % modulus
    retval2 = (val2-((retval1*val1) % modulus)) % modulus
    return (retval1, retval2)

# "This code calculates the Seed of the LCG if nth number is known
# Just a cheap reversal of the LCG"
def calcSeed(a, k, modulus, nr, nth):
    retval = nr
    for i in range(0, nth):
        retval -= k
        retval %= modulus
        # multiply by the inverse -> in the original paper this was a neat divide... lol
        retval *= modinv(a, modulus)
        retval %= modulus
    return retval

# stolen from https://stackoverflow.com/a/9758173 (Märt Bakhoff) as the built-in pow(-1) trick doesn't work with large ints
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def giveMeSeed(lcgoutput):
    outputcount = len(lcgoutput)
    detlistlength = outputcount - 3
    detlist = [None] * detlistlength
    print("calculating determinate")
    for i in range(0, detlistlength):
        detlist[i] = calcDet(lcgoutput[i],lcgoutput[i+1],lcgoutput[i+2],lcgoutput[i+3])

    print("calculating modulus")
    modulus = getModulus(detlist)

    print("verifying modulus")
    for i in range(0, outputcount):
        if(modulus < lcgoutput[i]):
            print("Modulus is too small (" + str(modulus) + "), probably no LCG")
            exit(-1)
    
    print("executing linear solution solve")
    (a, k) = linsolve(lcgoutput[0],lcgoutput[1],lcgoutput[2],modulus)
    print("The LCG function is : x[n] = ( " + str(a) + "*x[n-1] + " + str(k) + " ) % " + str(modulus))
    seed = calcSeed(a,k,modulus,lcgoutput[outputcount-1],outputcount)
    return seed

def generateTestLGCOutput():
    outputcount = 6
    detlistlength = outputcount - 3
    lcgoutput = [None] * outputcount # "lcgoutput contains the collected consecutive lcg output values"
    detlist = [None] * detlistlength

    random_moduli = [18446744011,18446744023,18446744059,18446744089,18446744093,18446744123,18446744137,18446744143,18446744201,18446744227,18446744243,18446744249,18446744291,18446744317,18446744363,18446744413,18446744443,18446744447,18446744479,18446744597,18446744599,18446744609,18446744621,18446744629,18446744653,18446744677,18446744741,18446744749,18446744779,18446744791,18446744801,18446744839,18446744861,18446744873,18446744941,18446744963,18446744971,18446745011,18446745043,18446745059,18446745073,18446745089,18446745091,18446745113,18446745179,18446745181,18446745193,18446745217,18446745253,18446745257,18446745281,18446745287,18446745307,18446745329,18446745353,18446745391,18446745409,18446745413,18446745437,18446745451,18446745463,18446745469,18446745511,18446745521,18446745523,18446745539,18446745547,18446745557,18446745589,18446745613,18446745617,18446745619,18446745623,18446745659,18446745671,18446745689,18446745799,18446745803,18446745817,18446745851,18446745869,18446745893,18446745901,18446745991,18446746061,18446746069,18446746081,18446746207,18446746211,18446746237,18446746247,18446746249,18446746259,18446746319,18446746337,18446746361,18446746379,18446746403,18446746441,18446746457,18446746459,18446746471,18446746481,18446746489,18446746519,18446746523,18446746531,18446746567,18446746583,18446746621,18446746639,18446746679,18446746697,18446746711,18446746783,18446746789,18446746841,18446746861,18446746867,18446746889,18446746897,18446746939,18446747009,18446747023,18446747051,18446747119,18446747153,18446747171,18446747173,18446747177,18446747251,18446747287,18446747321,18446747323,18446747383,18446747387,18446747401,18446747411,18446747419,18446747437,18446747441,18446747471,18446747519,18446747521,18446747537,18446747551,18446747567,18446747591,18446747609,18446747621,18446747681,18446747699,18446747701,18446747773,18446747819,18446747863,18446747909,18446747927,18446747929,18446747933,18446747993,18446748007,18446748049,18446748053,18446748071,18446748097,18446748107,18446748119,18446748143,18446748193,18446748223,18446748247,18446748343,18446748391,18446748457,18446748461,18446748473,18446748479,18446748487,18446748499,18446748503,18446748521,18446748547,18446748553,18446748563,18446748583,18446748599,18446748623,18446748647,18446748653,18446748701,18446748713,18446748731,18446748763,18446748779,18446748787,18446748839,18446748917,18446748919,18446748953]

    rng_mod = random.choice(random_moduli)
    mul = round(random.random() * (2 ** 32))
    add = round(random.random() * (2 ** 32))
    in_seed = round(random.random() * (2 ** 32))
    print("LCG init: (" + str(mul) + " * " + str(in_seed) + ") + " + str(add) + " mod " + str(rng_mod))
    print("")

    # "Basic Linear Congruential Generator"
    result = in_seed
    for i in range(0, outputcount):
        result = mul*result+add
        result %= rng_mod
        lcgoutput[i] = result
        print(result)
    # "------------------------------------"
    print()
    return lcgoutput

# end transcription
#########################################################################################################################################################################

if __name__ == "__main__":
    lcgoutput = generateTestLGCOutput()
    print("The Seed used was: " + str(giveMeSeed(lcgoutput)))
    exit(0)