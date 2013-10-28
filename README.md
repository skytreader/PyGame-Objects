The most awesome framework for PyGame you will ever encounter!

**But** it's not there yet. Right now, it's just a simple abstraction for some commmon code patterns I find while using PyGame.

**Built-on:**
* Python 2.6.5
* PyGame 1.9.1release; having
* SDL 1.2.14

Yep. I'm using Python 2.x because I can't get Python 3 to work with PyGame in Ubuntu.

# Current Status
I'm currently adding new features (see "helpers" directory and "tests/color\_blocks").
The product of my last dev cycle (a.k.a Julython 2012) is tagged as "Milestone1".

Right now, I'm working on adding extra game-making functionalities; stuff that
will maybe come useful if you do an RPG, platformer, arcade, etc., type of game.
I'm also working on adding new native drawing functionalities.

# File Organization
`components` houses the main framework. `sample_sprites` contains the sprites I
used for the test and demo files. `tests` contains, well, tests.

Since I tried to follow PEP 328, it may not be that straightforward to run the
tests. For convenience, navigate to the `runscripts` directory, pick the test
(as directories) you would like to run, and execute the runscripts from there.

The tests were written after every feature I finished. The tests are a mix of demos
and unit tests. Every now and then, I also write some mini-games to compile
demonstrations of some feature I'm working on.

## Monster Shooter Test
Just a simple game, with a simple set of rules it's virtually impossible to lose.
Keep shooting (with the `enter`) key. One monster is equivalent to one point.
Get hit by a monster and it will cost you one point (deduct one to current score).
You lose when your score becomes less than zero. And oh, move using the up and
down keys.

If you look at the code, this is a very simple version of what I originally had
in mind; maybe, some other time, for some other iteration of PyGame Objects. If
you look at my commit history, yes, this was supposed to be a clone of Plants vs
Zombies, but it ended up as a simple shoot-em-up.

## Color Blocks Game
Yet another common game you'd find at almost all Flash-game sites. I created
this mini-game to test the grid helper library I am working on. I'm not yet quite
done with the grid library but for a proof-of-concept, I'm quite satisfied with
this.

# Git Organization
Documentation is at the wiki. My todo list I made as issues. I am currently
working to make the documentation comprehensive (no more peeking at the framework
code!). However, something I was not able to forsee is that, the documentation
for Milestone 1 and for the code at the repo head has been mixed at the wiki.
Fortunately, they are not yet that different from each other and when and where
they differ, it is easy to note. In the near future, I plan to include markdown
files of the docs along with the code.
