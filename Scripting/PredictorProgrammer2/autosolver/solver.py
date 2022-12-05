#!/usr/local/bin/python3
from operator import contains
import socket
import time
import sys
import getopt
import os
from datetime import datetime

TIME_SCALE=10000
DEBUG_MODE=False
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
    int(os.getenv('CHALLENGE_2_PORT', 65001)),
    int(os.getenv('CHALLENGE_3_PORT', 65002))
]
challenge_domains = [
    'challenge-2'
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

flag = "sun{well_i_guess_it_was_time}"

def knuth_linear_congruential_generator(state):
    return ((state * 6364136223846793005) + 1442695040888963407) % (2 ** 64)

class OriginalSeedAndNextSeed:
    def __init__(self, original_seed):
        self.original_seed = original_seed
        self.next_seed = knuth_linear_congruential_generator(original_seed)
    
    def get_orig_seed(self):
        return self.original_seed

    def update_next_seed(self):
        self.next_seed = knuth_linear_congruential_generator(self.next_seed)
        return self
    
    def get_next_seed(self):
        return self.next_seed
    
    def __str__(self):
        return f"{(self.original_seed, self.next_seed)}"
    
    def __repr__(self):
        return f"<OriginalSeedAndNextSeed original_seed:{self.original_seed} next_seed:{self.next_seed}>"

def update_rng_list(orig_and_next_seed_list):
    return list(map(lambda x : x.update_next_seed(), orig_and_next_seed_list))

def find_mid_rng(orig_and_next_seed_list):
    generated_list = sorted(map(lambda x : x.get_next_seed(), orig_and_next_seed_list))
    return generated_list[len(generated_list) // 2]
    #return orig_and_next_seed_list[0].get_next_seed()

def debug_find_associated_value(current_seed, orig_and_current_seed_list):
    return list(filter(lambda x : x.get_next_seed() == current_seed, orig_and_current_seed_list))[0].get_orig_seed()

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
    while (not "date is" in intro):
        intro = client.recv(80000).decode('utf-8')
    
    print(f"intro: '''{str(intro)}'''")

    date = datetime.strptime(intro.split(sep="date is ")[1].split(sep='date is ')[0].split(sep=', you have')[0], "%a, %d %b %Y %H:%M:%S %z")
    utc_date = round(date.timestamp())
    ms_utc_date_min = (utc_date) * TIME_SCALE
    ms_utc_date_max = (utc_date + 1) * TIME_SCALE

    #real_seed = int(intro.split(sep="PLEASE REMOVE ")[1].split(sep="\n")[0])

    #print(f"utc {utc_date} min {ms_utc_date_min} max {ms_utc_date_max} real_seed {real_seed}")

    #if (real_seed < ms_utc_date_min or real_seed > ms_utc_date_max):
        #print(f"❌ PredictorProgrammer Challenge 2 bad seed! {datetime.utcnow().isoformat()}Z!")

    seed = -1
    feedback = ""

    seed_list = list(map(lambda x : OriginalSeedAndNextSeed(x), range(ms_utc_date_min, ms_utc_date_max)))
    if DEBUG_MODE:
        print(seed_list)
    while len(seed_list) > 0:
        next_seed = find_mid_rng(seed_list)

        # remove the intro nonsense
        while (not "18446744073709551615" in intro):
            intro = client.recv(80000).decode('utf-8')

        # send the expected value and get the key
        print(f"sending expected {next_seed}, think it's {debug_find_associated_value(next_seed, seed_list)}")
        #print(f"sending expected {next_seed}")
        client.send(str.encode(str(next_seed) + '\n'))

        
        # parse the expected message
        feedback = ""
        while not "number am I" in feedback and not "sun{" in feedback:
            feedback += client.recv(80000).decode('utf-8')
        print(f"feedback: {feedback}")
        
        #print(f"real_seed value = {list(filter(lambda x: x.get_orig_seed() == real_seed, seed_list))}")
        # binary search for the value: eliminate the seeds that produced values too big or too small until we find our real seed
        if "too small" in feedback:
            seed_list = list(filter(lambda x: x.get_next_seed() > next_seed, seed_list))
            if DEBUG_MODE:
                print(seed_list)
        elif "too big" in feedback:
            seed_list = list(filter(lambda x: x.get_next_seed() < next_seed, seed_list))
            if DEBUG_MODE:
                print(seed_list)
        elif "Lucky guess" in feedback:
            seed = next_seed
            break
        seed_list = update_rng_list(seed_list)
        
        #if len(list(filter(lambda x : x.get_orig_seed() == real_seed, seed_list))) != 1:
            #print(f"❌ PredictorProgrammer Challenge 2 eliminated seed, expected {real_seed} valid but eliminated! {datetime.utcnow().isoformat()}Z!")

        print(f"len remaining: {len(seed_list)}")
        if DEBUG_MODE:
            print(seed_list)
        
    if seed == -1:
        print("uh oh failed seed detect!")
        print(f"PredictorProgrammer Challenge 1 is down!")
        exit(1)
    
    while (not "sun" in feedback and not "wrong" in feedback):
        print(feedback)
        print(f"sending final expected {seed}")
        seed = knuth_linear_congruential_generator(seed)
        client.send(str.encode(str(seed) + '\n'))
        time.sleep(0.1)
        feedback = client.recv(80000).decode('utf-8')
    # race exists where the last recv steals all the info from the server
    print(f"key is possibly in '{feedback}'")
    if not flag in feedback:
        print(f"❌ PredictorProgrammer Challenge 2 is down as of {datetime.utcnow().isoformat()}Z!")
        nonsense = str(client.recv(80000))
        print(nonsense)
        exit(1)

    print(
        f"Verified key from challenge produces CTFd flag {feedback} contains {flag}"
    )

    if repeat:
        print(f"✔️  PredictorProgrammer Challenge 2 still up as of {datetime.utcnow().isoformat()}Z... sleeping for 30 seconds...")
        time.sleep(30)
    else:
        print(f"✔️  PredictorProgrammer Challenge 2 still up as of {datetime.utcnow().isoformat()}Z... exiting.")
        exit(0)
