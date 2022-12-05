#!/usr/local/bin/python3
import socket
import time
import sys
import getopt
import os
from datetime import datetime

sys.stdout.reconfigure(line_buffering=True)

# usage:
# when debugging locally and don't want it to repeat:
# python solver.py --localhost --no-repeat
# when debugging a real-server challenge and want it to repeat:
# python solver.py
# when debugging a real-server challenge and don't want it to repeat:
# python solver.py --no-repeat
# skip the first sleep (helps with service synchronization)
# python solver.py --skip-first-sleep
challenge_ports = [
    int(os.getenv('CHALLENGE_1_PORT', 65000)),
    int(os.getenv('CHALLENGE_2_PORT', 65001))
]
challenge_domains = [
    'challenge-1'
]
repeat = True
first_sleep = True

if len(sys.argv) > 1:
    print(f"Detected arguments: {sys.argv[1:]}")
    try:
        # modified from https://www.tutorialspoint.com/python3/python_command_line_arguments.htm
        opts, args = getopt.getopt(sys.argv[1:], "lns",
                                   ["localhost", "no-repeat", "skip-first-sleep"])
        for opt, arg in opts:
            if opt == '-l' or opt == '--localhost':
                challenge_domains = ["localhost", "localhost", "localhost"]
                print("Using localhost instead of challenge servers")
            elif opt == "-n" or opt == "--no-repeat":
                repeat = False
                print("Only executing auto-solve once.")
            elif opt == "-s" or opt == "--skip-first-sleep":
                first_sleep = False
            else:
                print(f"Unknown argument {opt} passed, ignoring.")
    except getopt.GetoptError:
        print(
            "Unknown argument given. Continuing with normal DNS resolution instead."
        )

print(f"Challenge domains chosen: {challenge_domains}")
print(f"Challenge ports chosen: {challenge_ports}")

# sleep for 10 seconds for the other docker containers to start up
if first_sleep:
    print(f"Autosolver up as of {datetime.utcnow().isoformat()}Z... sleeping for 10 seconds to allow other services time to start (skip this with the --skip-first-sleep option)")
    time.sleep(10)
    print("Autosolver starting solve.")

flag = "sun{oops_i_thought_i_was_in_release}"

def knuth_linear_congruential_generator(state):
    return ((state * 6364136223846793005) + 1442695040888963407) % (2 ** 64)

while True:
    found_flag = ""
    # copied from https://stackoverflow.com/questions/48390709/streaming-tcp-data-to-a-client-with-python
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ip = socket.gethostbyname(challenge_domains[0])
    except socket.gaierror:
        print(
            f"Challenge DNS servers may be down, could not resolve {challenge_domains[0]}"
        )
        exit(1)

    port = challenge_ports[0]
    address = (ip, port)

    try:
        client.connect(address)
    except ConnectionError as e:
        print(
            f"Fatal error connecting to {address}! Connection error {e}.")
        exit(1)

    # remove the intro nonsense
    intro = ""
    while (not "debugggg" in intro):
        intro = client.recv(80000).decode('utf-8')
    
    print(f"intro: '''{str(intro)}'''")

    seed = int(intro.split(sep="= ")[1].split()[0])

    expected = knuth_linear_congruential_generator(seed)

    # remove the intro nonsense
    while (not "18446744073709551615" in intro):
        intro = client.recv(80000).decode('utf-8')

    # send the expected value and get the key
    print(f"sending expected {expected}")
    client.send(str.encode(str(expected) + '\n'))
    
    # get rid of one seed message and then get the rest of the stuff
    key = client.recv(80000).decode('utf-8')
    key = key + client.recv(80000).decode('utf-8').rstrip()

    # race exists where the last recv steals all the info from the server
    print(f"key is '{key}'")
    if not flag in key:
        print(f"PredictorProgrammer Challenge 1 is down!")
        nonsense = str(client.recv(80000))
        print(nonsense)
        exit(1)

    print(
        f"Verified key from challenge produces CTFd flag {found_flag} = {flag}"
    )

    if repeat:
        print(f"✔️  challenges still up as of {datetime.utcnow().isoformat()}Z... sleeping for 30 seconds...")
        time.sleep(30)
    else:
        print(f"✔️  Challenges still up as of {datetime.utcnow().isoformat()}Z... exiting.")
        exit(0)
