# Chapter 7: The Code

There was very little that Roy felt he could do to solve the problem. It felt intractable. He called Kara over. "Hey Kara. Look at this problem. Our navigation software isn't able to decipher this. What are we supposed to do?"

"You're only looking at the extended kalman filter. Have we considered other ones like particle filters?"

"Never used them before and I'm sure our navigation software don't use that either."

"It's not as hard as it might seem. I think I can code one up."

Roy scoffed. "You're going to write an entirely new piece of flight software while we're flying on this ship? This sounds insane." 

"Now Roy I know that you've a lot more experience but have you worked with particle filters?"

Roy shook his head. Kara smiled. "In that case, just have some faith in me. We do have an intelligent AI agent onboard which can help speed things up considerably. Our onboard software was designed to be malleable to some extent."

Roy sounded skeptical but a bit of curiosity was leaking through. He asked. "Can you explain in basic terms to me what that is?"

"Sure, let me demonstrate with some simple code. I'll write it in Python which I know you know."

```
import numpy as np
import matplotlib.pyplot as plt

# Initialize parameters
T = 15   # number of time steps
Q = 1.0  # process noise variance
R = 4.0  # measurement noise variance
N = 200  # number of particles
```