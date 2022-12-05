# PredictorProgrammer
## Take that, friends and siblings!

Have you ever played "Guess the Number?"

You know, "I'm thinking of a number from 1 to X, where X is a non-real number with some imaginary parts and could be transcendental but not e or pi?"

No? Gee I must have weird friends.

What about "I'm thinking of a number from 1 to 10?"

Oh? You have?

Well have I got a challenge for you!

Last year, I procrastinated my security system, and took security in the challenge to the cliff of failure.

Heh heh, turns out eval wasn't safe to use... ever.

This year we take one step further! *_Minus the whole "user sends executable code to us that we then use python to execute," and all. That was a **minor** mistake._

Visit `predictor.2022.sunshinectf.org 65000`, and play a game of predicting the future!

But don't worry that this game will get old! The flags in this game are split into three kingdoms, with one flag in each... you'll never find them all! And since it's random, no two games will ever be alike!

Flag will be given by our backend in the standard `sun{}` format!

## Notes

I am not unreasonable.

All I ask is you predict the future with 100% accuracy.

That's hard, that's why I give you a couple chances to get it wrong.

Once you get a few numbers I feel you'll get the hang of it.

Just don't use the previous numbers to predict the state of the RNG, that would totally not be predicting the future, as the state is set from the start, so you'd be predicting the past! And it would _ruin_ the whole concept of this challenge and make it an exercise in math and googling how to break linear congruential generators! That's super boring, this is _strictly_ about predicting the future, which is fun!

## Example Usages

"Hi, I'm thinking of a number from 1 to 31"
```python
7
```
Wrong. I was thinking of 17. You must not be from Florida!

...


8
Correct! You've guessed 3 numbers correctly, and have 1 life left! Only 16 more correct answers left to guess!

Note: In the future we may change the support structure if we find there's security issues with them.
