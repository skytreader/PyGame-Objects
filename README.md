Nothing grand here (yet). Just a simple abstraction for some commmon code patterns I find while using PyGame.

**Built-on:**
* Python 2.6.5
* PyGame 1.9.1release; having
* SDL 1.2.14

Yep. I'm using Python 2.x because I can't get Python 3 to work with PyGame in Ubuntu.

# Current Status
I'm currently adding new features (see "helpers" directory and "tests/color_blocks"). The product of my last dev cycle (a.k.a Julython 2012) is tagged as "Milestone1".

# File Organization
`components` houses the main framework. `sample_sprites` contains the sprites I used for the test and demo files. `tests` contains, well, tests.

The tests were written after every feature I finished. The tests are a mix of demos and unit tests. There is also one large demo that encompasses all that I have so far---the monster shooter test.

## Monster Shooter Test
Just a simple game, with a simple set of rules it's virtually impossible to lose. Keep shooting (with the `enter`) key. One monster is equivalent to one point. Get hit by a monster and it will cost you one point (deduct one to current score). You lose when your score becomes less than zero. And oh, move using the up and down keys.

If you look at the code, this is a very simple version of what I originally had in mind; maybe, some other time, for some other iteration of PyGame Objects. If you look at my commit history, yes, this was supposed to be a clone of Plants vs Zombies, but it ended up as a simple shoot-em-up.

# Git Organization
Documentation is at the wiki though it is not very comprehensive; the inline docs will be far more informative. My todo list I made as issues.
