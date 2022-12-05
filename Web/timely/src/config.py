import hashlib
import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret Key for sessions
SECRET_KEY = str(os.urandom(15))

# ASDF
plaintext = "OMFG_IS_THIS_NOT_EVEN_A_GAMING_THEMED_CHALLENGE_IN_A_GAMING_THEMED_CTF"
HASH = str(hashlib.sha1(plaintext.encode()).hexdigest())
print(HASH)
# HASH = "f55627ebc3997247413a4972baa5525d6d730370"

with open("flag.txt", "r") as file:
    FLAG = file.readlines()[0]
# FLAG = "SUN{ci+ypopi56e5+pop2022}"
