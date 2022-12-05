#!/bin/sh
[ "$(curl --silent educashun-game.2022.sunshinectf.org/login.html | grep -e 'sun{' | sed -re 's/.*sun\{(.*)\}.*/sun{\1}/')" = "$(cat ./flag.txt)" ]