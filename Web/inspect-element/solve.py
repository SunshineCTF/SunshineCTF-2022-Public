#!/usr/bin/env python3
# Inspect Element - the flag is hidden in a text="sun{...}" attribute on the
# login page; just "view source" (here: fetch it and grep). Env-driven $URL so
# `pwnmake check` can point us at the started container.
import os, sys, re, urllib.request

URL = os.environ.get("URL") or (sys.argv[1] if len(sys.argv) > 1 else "https://inspect-element.ctf.hackucf.org")
html = urllib.request.urlopen(URL.rstrip("/") + "/login.html", timeout=15).read().decode(errors="replace")
m = re.search(r"sun\{[^}]*\}", html)
print(m.group(0) if m else "NO FLAG FOUND")
