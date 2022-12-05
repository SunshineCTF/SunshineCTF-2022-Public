# Writeup
## Predictor Programmer 1
This one's a simple guess-the-number.

We're given the following source code:
```python
def knuth_linear_congruential_generator(state):
    return (state * 6364136223846793005) + 1442695040888963407 % (2 ** 64)
```
And the initial state:
```
#debugggg seed = <value>
```
Hence if we just calculate the value in python, we'll guess the next number.

And that gives us the flag.