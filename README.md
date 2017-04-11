The most awesome framework for PyGame you will ever encounter!
[![Build Status](https://travis-ci.org/skytreader/PyGame-Objects.svg?branch=master)](https://travis-ci.org/skytreader/PyGame-Objects)
[![Coverage Status](https://coveralls.io/repos/github/skytreader/PyGame-Objects/badge.svg?branch=master)](https://coveralls.io/github/skytreader/PyGame-Objects?branch=master)

**But** it's not there yet. Right now, it's just a simple abstraction for some
commmon code patterns I find while using PyGame.

**Built on:** see `.travis.yml` as well as `requirements.txt`. Wonder why, after
all these years, PyGame is still not reachable via `pip`.

Yep. I'm using Python 2.x because I can't get Python 3 to work with PyGame in Ubuntu.

# Development
Aside from `.travis.yml`, the Dockerfile is provided for development. You can
also pull the image via

    docker run skytreader/pygame-objects:stablest

One of these days, I might actually follow Docker conventions of tagging my
images as "latest".

**IMPORTANT; Continue reading:** Note that the above command will only pull the
image for you, to be able to do anything of interest, you need a bit more Docker
arcana. Specifically, you need to run Docker with X11 forwarding:

    docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -it -d skytreader/pygame-objects:stablest /bin/bash

This gives a container ID which you can then use to execute a Docker shell that
which can run the games:

    docker exec -it <container_id> /bin/bash

A truncated, but no less valid version of the container id can also be obtained
via `docker ps`.

# Current Status
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

# License

All code in master (except when noted) are licensed under MIT.

All sprites under `sample_sprites/tiles` are licensed under a
[Creative Commons Attribution-ShareAlike 4.0](http://creativecommons.org/licenses/by-sa/4.0/)
license.
