# Writeup
## Predictor Programmer 2
This one's more difficult than PredictorProgrammer 1. We're heavily hinted that the seed is the current time in hundreds of microseconds.

Hence, we have to convert the time (given in UTZ zulu time) to UTC seconds, and then multiply the result by 10,000 to get the time in hundreds of microseconds.

While this is good and all, this results in a time window of 10,000 seeds!

As the server only tells us if the guess is too high or too low, we have to keep sending the next best guess, and eliminate the outliers with a binary search.

We're given the following source code:
```python
def knuth_linear_congruential_generator(state):
    return (state * 6364136223846793005) + 1442695040888963407 % (2 ** 64)
```
And the initial state:
```
The current date is <ISO TIMESTAMP>, you have...
```
resulting in binary search code like
```python
while len(seed_list) > 0:
    next_seed = find_mid_rng(seed_list)

    # remove the intro nonsense
    while (not "18446744073709551615" in intro):
        intro = client.recv(80000).decode('utf-8')

    # send the expected value and get the key
    print(f"sending expected {next_seed}, think it's {debug_find_associated_value(next_seed, seed_list)}")
    while not "number am I" in feedback and not "sun{" in feedback:
        feedback += client.recv(80000).decode('utf-8')
    print(f"feedback: {feedback}")

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
```
As the server is cycling through its values though, we have to continue generating new values. So while more complicated than a binary search, it's still pretty much just a binary search.