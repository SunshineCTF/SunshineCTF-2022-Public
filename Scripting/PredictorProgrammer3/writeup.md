# Writeup
## Predictor Programmer 3
This one's arguably not more difficult than Predictor Programmer 2.

We're given the following source code:
```python
modulus = secrets.choice(random_prime_moduli)
multiplier = secrets.randbelow(modulus)
adder = secrets.randbelow(modulus)
seed = secrets.whatever(modulus)
# ITS NOT SECURE WHATEVS BRING IT
def some_random_number_generator(state_I_GUESS):
    return (state_I_GUESS * multiplier) + adder %% modulus
```
And the initial state:
```
I was thinking of <number 1>...
I was thinking of <number 2>...
I was thinking of <number 3>...
I was thinking of <number 4>...
I was thinking of <number 5>...
I was thinking of <number 6>...
```
And we're told to find the SEED that produced these numbers.

As such we have to research how to reverse LCGs.

Doing some searching finds:
https://www.violentlymild.com/posts/reverse-engineering-linear-congruential-generators/
and potentially http://www.reteam.org/papers/e59.pdf.

Implementing the algorithm specified by RETeam results in a successful crack of the numbers.
