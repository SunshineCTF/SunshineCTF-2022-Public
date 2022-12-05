#!/usr/local/bin/python3
import os
import sys
import multiprocessing
import time
import secrets

# 200 random primes
random_moduli = [18446744011,18446744023,18446744059,18446744089,18446744093,18446744123,18446744137,18446744143,18446744201,18446744227,18446744243,18446744249,18446744291,18446744317,18446744363,18446744413,18446744443,18446744447,18446744479,18446744597,18446744599,18446744609,18446744621,18446744629,18446744653,18446744677,18446744741,18446744749,18446744779,18446744791,18446744801,18446744839,18446744861,18446744873,18446744941,18446744963,18446744971,18446745011,18446745043,18446745059,18446745073,18446745089,18446745091,18446745113,18446745179,18446745181,18446745193,18446745217,18446745253,18446745257,18446745281,18446745287,18446745307,18446745329,18446745353,18446745391,18446745409,18446745413,18446745437,18446745451,18446745463,18446745469,18446745511,18446745521,18446745523,18446745539,18446745547,18446745557,18446745589,18446745613,18446745617,18446745619,18446745623,18446745659,18446745671,18446745689,18446745799,18446745803,18446745817,18446745851,18446745869,18446745893,18446745901,18446745991,18446746061,18446746069,18446746081,18446746207,18446746211,18446746237,18446746247,18446746249,18446746259,18446746319,18446746337,18446746361,18446746379,18446746403,18446746441,18446746457,18446746459,18446746471,18446746481,18446746489,18446746519,18446746523,18446746531,18446746567,18446746583,18446746621,18446746639,18446746679,18446746697,18446746711,18446746783,18446746789,18446746841,18446746861,18446746867,18446746889,18446746897,18446746939,18446747009,18446747023,18446747051,18446747119,18446747153,18446747171,18446747173,18446747177,18446747251,18446747287,18446747321,18446747323,18446747383,18446747387,18446747401,18446747411,18446747419,18446747437,18446747441,18446747471,18446747519,18446747521,18446747537,18446747551,18446747567,18446747591,18446747609,18446747621,18446747681,18446747699,18446747701,18446747773,18446747819,18446747863,18446747909,18446747927,18446747929,18446747933,18446747993,18446748007,18446748049,18446748053,18446748071,18446748097,18446748107,18446748119,18446748143,18446748193,18446748223,18446748247,18446748343,18446748391,18446748457,18446748461,18446748473,18446748479,18446748487,18446748499,18446748503,18446748521,18446748547,18446748553,18446748563,18446748583,18446748599,18446748623,18446748647,18446748653,18446748701,18446748713,18446748731,18446748763,18446748779,18446748787,18446748839,18446748917,18446748919,18446748953]

flag_p3 = open('./key', "rb").read()

def test_client(stdinput):
    modulus = secrets.choice(random_moduli)
    seed = secrets.randbelow(modulus)
    multiplier = secrets.randbelow(modulus)
    adder = secrets.randbelow(modulus)

    time_in_seconds = time.time()
    pretty_print_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(time_in_seconds))

    print("#debugggg seed = CENSORED\n")
    print("The current date is " + pretty_print_time + ", you have 60 seconds to guess the SEED number correctly (yeah I don't use the time as a seed anymore, but I think this looks cool).")

    next_number = some_random_number_generator(seed, multiplier, adder, modulus)
    print("Predict the PAST SEED... if you dare!\nHere are your numbers from the future...")

    for _ in range(0, 6):
        print("I was thinking of " + str(next_number) + "...")
        next_number = some_random_number_generator(next_number, multiplier, adder, modulus)

    print("Now that you have your numbers... what was the PAST SEED I was thinking of?")
    guess = int(stdinput.readline())
    if guess == seed:
        print("Well these jokes are old but they still check out...")
        sys.exit(0)
    else:
        print("Looks like those were not the DONT SUE ME DISNEY ITS JUST A REFERENCE I was looking for...")
        sys.exit(1)

# if knuth made it it must be secure!
def some_random_number_generator(state, multiplier, adder, modulus):
    return ((state * multiplier) + adder) % modulus

# launches a client session for a given level.
def client_thread():
    try:
        message = 'Take three...\n'
        message += '...\n'
        message += '...\n'
        message += 'Well this time I don\'t use the time as a secure init... heh... heh...\n'
        message += 'Apparently there\'s something called the \'secrets\' module in python\n'
        message += 'I could just use it directly, but I want to play one... last... game of guessing!\n'
        message += 'Tell you what, I\'ll give you one life to guess the SEED now.\n'
        message += '...But to help you on your way I\'ll give you 6 numbers...\n'
        message += 'I also read in a paper somewhere (idk mid 2000s... been a while) that that\'s\n'
        message += ' enough numbers to crack open any old linear congrential generator...\n'
        message += '...\n'
        message += '...\n'
        message += 'Please don\'t... I really, really want to make sure you can predict the PAST...\n'
        message += '\n'
        message += 'Ah who cares heres the code.\n'
        message +="""modulus = secrets.choice(random_prime_moduli)
multiplier = secrets.randbelow(modulus)
adder = secrets.randbelow(modulus)
seed = secrets.whatever(modulus)
# ITS NOT SECURE WHATEVS BRING IT
def some_random_number_generator(state_I_GUESS):
    return (state_I_GUESS * multiplier) + adder %% modulus\n"""
        print(message)

        # thanks to jfs https://stackoverflow.com/a/8981813
        new_stdin = os.fdopen(os.dup(sys.stdin.fileno()))
        try:
            # Eh not really needed but it'll distract them longer if they think they can bring the challenge down somehow.
            client_process = multiprocessing.Process(target=test_client, args=[new_stdin])
            
            client_process.start()
            client_process.join(30)

            if client_process.is_alive():
                client_process.terminate()
                print("Too slow! You must not be from Florida!")
                raise RuntimeWarning()

            # thanks to ATOzTOA (https://stackoverflow.com/a/14924210) for helping with the multiprocessing code
            if client_process.exitcode != 0:
                print("Eh... wrong answer. You must not be from Florida!")
                raise RuntimeWarning()
        finally:
            new_stdin.close()
            
        print("\n...")
        print("fine. See https://youtu.be/AITqA6OC9aA.")
        print("\nIf you solved this without http://www.reteam.org/papers/e59.pdf sorry not sorry.")
        print("\n...")
        
        print("\n... oh well here's your last key, as promised:")
        print(flag_p3)
        print("\nI know I said you wouldn't get anything special for finishing all three challenges...\n")
        print("And that's correct! Goodbye!")
        return 0

    except RuntimeWarning:
        print("Come visit Florida again some time!")
        return 0
    except KeyboardInterrupt:
        print("Killing server", file=sys.stderr)
        print("Server killed by Sunshine CTF admins, technical difficulties currently with this challenge, please come back soon. This is not part of the challenge... sorry. :(")
        return 0

client_thread()