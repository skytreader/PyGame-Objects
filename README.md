# PyGame Objects

> Want a sample on how to work with this framework? Check out the docs in the
> [wiki](https://github.com/skytreader/PyGame-Objects/wiki), particularly the
> [Walkthrough](https://github.com/skytreader/PyGame-Objects/wiki/Framework-Walkthrough)

The most awesome framework for PyGame you will ever encounter!
[![Build Status](https://travis-ci.org/skytreader/PyGame-Objects.svg?branch=master)](https://travis-ci.org/skytreader/PyGame-Objects)
[![Coverage Status](https://coveralls.io/repos/github/skytreader/PyGame-Objects/badge.svg?branch=master)](https://coveralls.io/github/skytreader/PyGame-Objects?branch=master)

**But** it's not there yet. Right now, it's just a simple abstraction for some
commmon code patterns I find while using PyGame.

**Built on:** see `.travis.yml` as well as `requirements.txt`. Needs Python 3.7+
as this relies on language features only available from there.

# Development

Aside from `.travis.yml`, the Dockerfile is provided for development. The
Dockerfile takes an argument `userid` which should be a user id outside the
container that has access to `/tmp/.X11-unix`. If you are in a graphical desktop
environment, it would suffice to pass the `$UID` environment variable like so,

    docker build -t pygame-objects --build-arg userid=$UID .

You can also pull the image via

    docker run skytreader/pygame-objects:latest

At this point, you only have the image. To develop and run games with it, you
should use the provided `duckrunner` script. It takes the package path to the
script that invokes your game loop. For example, to run the included snake game,
call `duckrunner demo.snake.game`.

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
