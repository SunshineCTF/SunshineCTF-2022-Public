#!/usr/local/bin/python3
from operator import contains
import socket
import time
import sys
import getopt
import os
from datetime import datetime
import seed_solver

sys.stdout.reconfigure(line_buffering=True)
DEBUG_MODE=False

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
    int(os.getenv('CHALLENGE_3_PORT', 65002))
]
challenge_domains = [
    'challenge-3'
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

flag = "sun{bah_figures_lcgs_are_not_cryptographically_secure}"

def die():
    print(f"❌ PredictorProgrammer Challenge 3 is down as of {datetime.utcnow().isoformat()}Z!")
    exit(1)

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
        die()

    port = challenge_ports[0]
    address = (ip, port)

    try:
        client.connect(address)
    except ConnectionError as e:
        print(
            f"Fatal error connecting to {address}! Connection error {e}.")
        die()

    # remove the intro nonsense
    intro = ""
    while (not "what was the PAST SEED I was thinking of" in intro):
        temp_print = client.recv(80000).decode('utf-8')
        print(temp_print)
        intro += temp_print

    initial_values=[]
    lines = intro.split(sep='\n')
    for line in lines:
        if "I was thinking of " in line:
            initial_values.append(int(line.split(sep="I was thinking of ")[1].split(sep='...')[0]))

    if len(initial_values) < 6:
        print(f"Missing initial values! Expected 6 initial values, found {len(initial_values)}")
        die()
                
    if DEBUG_MODE:
        print(initial_values)
    
    print("Calculating seed!")
    seed = seed_solver.giveMeSeed(initial_values)
    print(f"Seed calculated as {seed}")
    client.send(str.encode(str(seed) + '\n'))

    feedback=""
    while (not "sun" in feedback and not "wrong" in feedback):
        print(f"final feedback: {feedback}")
        feedback = client.recv(80000).decode('utf-8')
    
    # race exists where the last recv steals all the info from the server
    print(f"key is possibly in '{feedback}'")
    if not flag in feedback:
        nonsense = str(client.recv(80000))
        print(nonsense)
        die()

    print(
        f"Verified key from challenge produces CTFd flag {feedback} contains {flag}"
    )

    if repeat:
        print(f"✔️  PredictorProgrammer Challenge 3 still up as of {datetime.utcnow().isoformat()}Z... sleeping for 30 seconds...")
        time.sleep(30)
    else:
        print(f"✔️  PredictorProgrammer Challenge 3 still up as of {datetime.utcnow().isoformat()}Z... exiting.")
        exit(0)
