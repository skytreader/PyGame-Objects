#! usr/bin/env python

from components.image import Image

import os

import pygame

"""
Image exception test results.

Scenario: File specified does not exist.
In this case, the call to pygame.image.load ... already throws
an Exception and it is pointless to throw our own custom Exception.

Scenario: File specified is deleted after load.
Does not seem to affect program flow in any way.

Also, this resource does not seem to need closing.

@author Chad Estioco
"""

pygame.display.set_mode([500, 500])
nonexistent = Image(os.path.join("sample_sprites", "lalamon_clueless.png"));

# Set-up blocking code...
foo = input("Press enter when you have moved lalamon_clueless.png");

nonexistent.flip(True, False)

print("If you got here, deleting the resource does nothing.")
