# [PWN 50] CTF Simulator

Very easy challenge. Step 1 is to enter a team name that's at least 20 bytes
long to fill the `gs.name` buffer. This buffer is filled using `strncpy`, so
it will not be NUL-terminated. Then, when the name is printed out, the random
seed will be leaked. This seed can then be used by players to seed their own
RNG such that they'll know exactly what number they need to guess every time.
