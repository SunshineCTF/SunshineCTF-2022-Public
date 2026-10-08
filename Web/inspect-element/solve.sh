#!/bin/sh
# Inspect Element - the flag is hidden in a `text="sun{...}"` attribute on the
# login page; just view source. Pass a base URL, defaults to the archive host.
HOST="${1:-https://inspect-element.ctf.hackucf.org}"
[ "$(curl --silent "$HOST/login.html" | grep -e 'sun{' | sed -re 's/.*sun\{(.*)\}.*/sun{\1}/')" = "$(cat "$(dirname "$0")/flag.txt")" ]
