A testcase of HTM theory

NuPIC(http://www.numenta.org) implemented a model that mimic the core behaviour brain respond to universal inputs.

presume that all things well done, then we got a system which could respond to sensor input, yet passive, for the system lack it’s own motive.

pains and the desires are the compelling force  which droves livings to act.

so i build a testcase called snake game which introduced pain & desire in the system, hope it could help the snake adjust its act to get desire fulfilled and least pain.

in the game, the snake move around in an square splited into grids ,  within which food emerges randomly.if the snake catch the food, it’s desire score goes high, and if hit the wall, it feel pain. the vision, pain, desire, and direction control could be easily encoded into SDRs.

under this prediction, the system should evolve the snake to a food hunter, which expound a complete machine intelligence who would adapt to environment and avoid danger and pursue it’s own desire.

i’ve been work around with NuPIC for several days, still couldn’t figure out how to endow the snake to act based on the vision pain and desire it sensed, so it's tacked here. anyway, keep learning.

just run python snake_game.py.