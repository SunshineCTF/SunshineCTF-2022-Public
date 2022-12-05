#!/usr/local/bin/python3
import os
import sys
import multiprocessing
import time
import random

TIME_SCALE=10000

sys.stdout.reconfigure(line_buffering=True)
next_challenge_port = os.getenv('CHALLENGE_3_PORT', 65002)
next_challenge_domain = os.getenv('CHALLENGE_3_DOMAIN', 'predictor-sequel.2022.sunshinectf.org')
flag_p2 = open('./key', "rb").read()

def test_client(stdinput):
    seed = get_time_number()
    time_in_seconds = seed // TIME_SCALE
    pretty_print_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(time_in_seconds))
    lives = 16
    correct_responses = 0

    print("#debugggg seed = CENSORED\n")
    # print(seed)
    print("The current date is " + pretty_print_time + ", you have 30 seconds to guess the next number correctly.")
    
    while lives > 0 and correct_responses < 5:
        next_number = knuth_linear_congruential_generator(seed)
        print(f"Predict the future... if you dare!\nYou have {lives} lives left!\nWhat number am I thinking of, from 0 to 18446744073709551615:")

        guess = int(stdinput.readline())
        
        if guess < next_number:
            print(f"That number was too small. Generating another random number...")
            lives -= 1
        elif guess > next_number:
            print(f"That number was too big. Generating another random number...")
            lives -= 1
        else:
            print('Lucky guess for that number... I don\'t trust you, so I\'ll ask some more questions to be safe...')
            correct_responses += 1
        seed = next_number
    if lives > 0:
        print("Well these codes are old but they check out...")
        sys.exit(0)
    else:
        print("Looks like those were not the codes I was looking for...")
        sys.exit(1)

# we use the time as a "random number" as it's used by the second challenge.
def get_time_number():
    return round(time.time() * TIME_SCALE)

# if knuth made it it must be secure!
def knuth_linear_congruential_generator(state):
    return ((state * 6364136223846793005) + 1442695040888963407) % (2 ** 64)

# launches a client session for a given level.
def client_thread():
    try:
        message = 'So as it turns out leaving the debug print on was a mistake.\n'
        message += '...\n'
        message += 'Well no bother. This TIME I don\'t print the seed!\n'
        message += 'In fact, you\'ll never guess what the seed is this TIME!\n'
        message += 'And if you do... well don\'t tell anyone, especially since my server may have its own TIME...\n'
        message += 'And I\'d be stupid to use something predictable like TIME to predict the future...\n'
        message += 'There would be 100s of microseconds... uh I mean 100s of thousands of possibilities possible!\n'
        message += '...\n'
        message += 'Because I\'m so confident in this new system\'s security, this TIME I will give you SIXTEEN LIVES to make a guess...\n'
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
            client_process.join(60)

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
        
        print("\n... oh well here's your second key, as promised:")
        print(flag_p2)
        print("\nFine. I'll make a better game. Sequels are all the rage! 🔥🏰🔥")
        print(f"\n{next_challenge_domain} {next_challenge_port} holds your next clue.")
        return 0

    except RuntimeWarning:
        print("Come visit Florida again some time!")
        return 0
    except KeyboardInterrupt:
        print("Killing server", file=sys.stderr)
        print("Server killed by Sunshine CTF admins, technical difficulties currently with this challenge, please come back soon. This is not part of the challenge... sorry. :(")
        return 0

client_thread()