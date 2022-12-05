#!/usr/local/bin/python3
import os
import sys
import multiprocessing
import time
import random

sys.stdout.reconfigure(line_buffering=True)
next_challenge_port = os.getenv('CHALLENGE_2_PORT', 65001)
next_challenge_domain = os.getenv('CHALLENGE_2_DOMAIN', 'predictor-castle.2022.sunshinectf.org')
flag_p1 = open('./key', "rb").read()

def test_client(stdinput):
    seed = get_time_number()
    time_in_seconds = seed // 1000
    pretty_print_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(time_in_seconds))

    print("#debugggg seed = " + str(seed) + "\n")
    print("The current date is " + pretty_print_time + ", you have 30 seconds to guess the next number correctly.")
    next_number = knuth_linear_congruential_generator(seed)
    print("Predict the future... if you dare!\nWhat number am I thinking of, from 0 to 18446744073709551615:")
    guess = stdinput.readline()
    print("I was thinking of " + str(next_number) + "...")
    return guess == next_number

# we use the time as a "random number" as it's used by the second challenge.
def get_time_number():
    return round(time.time() * 1000)

# if knuth made it it must be secure!
def knuth_linear_congruential_generator(state):
    return ((state * 6364136223846793005) + 1442695040888963407) % (2 ** 64)

# launches a client session for a given level.
def client_thread():
    try:
        message = 'PredictorProgrammer... new and improved! No longer vulnerable to eval injection!\n'
        message += '...'
        message += 'oooooooh we are going to play a game... of Prediction!\n'
        message += 'Super duper easy! You have one life to get the answer correct!\n'
        message += 'If you get the answer correct... you\'ll receive a key, one of three.\n'
        message += 'A person who has all three keys... well... nothing special happens.\n'
        message += 'But back to prediction...\n'
        message += 'So we\'re on the up-and-level with each other, I\'m using this code to come up with a totally random number:\n'
        message += '\n'
        message +="""# if knuth made it it must be secure!
def knuth_linear_congruential_generator(state):
    return (state * 6364136223846793005) + 1442695040888963407 % (2 ** 64)\n"""
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
        print("\nHooooowwww? How did you solve it?")
        print("\n...")
        
        print("\n... oh well here's your first key, as promised:")
        print(flag_p1)
        print("\nFine. I'll make a better game. ONE WITH A PRINCESS IN ANOTHER CASTLE! 🔥🏰🔥")
        print(f"\n{next_challenge_domain} {next_challenge_port} holds your next key.")
        return 0

    except RuntimeWarning:
        print("Come visit Florida again some time!")
        return 0
    except KeyboardInterrupt:
        print("Killing server", file=sys.stderr)
        print("Server killed by Sunshine CTF admins, technical difficulties currently with this challenge, please come back soon. This is not part of the challenge... sorry. :(")
        return 0

client_thread()