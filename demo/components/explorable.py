from __future__ import division

from components.core import GameConfig, GameModel, GameScreen, GameLoopEvents, GameLoop
from components.image import Image
from pygame.sprite import Group

import os
import random

class ExplorableScreen(GameScreen):

    def __init__(self, config, model):
        super(ExplorableScreen, self).__init__(config, model)

    def setup(self):
        super(ExplorableScreen, self).setup()
        pastel_flowers = Image(os.path.join("sample_sprites", "tiles", "png", "pastel_flowers.png"))
        grass = Image(os.path.join("sample_sprites", "tiles", "png", "grass.png"))
        images = (pastel_flowers, grass)

        # XXX Just a demo, do not try this at home: this (rightly!) assumes that
        # pastel_flowers and grass have the same dimensions
        visible_width = int(self.screen_dimensions[GameConfig.WIDTH_INDEX] / pastel_flowers.width)
        visible_height = int(self.screen_dimensions[GameConfig.HEIGHT_INDEX] / pastel_flowers.height)
        area_tile_size = (visible_width + 2) * (visible_height + 2)
        self.tiles = Group()
        
        for i in range(area_tile_size):
            img = random.choice(images)
            img_xpos = img.width * (i % visible_width)
            img_ypos = img.height * (i % visible_height)

            self.tiles.add(img.clone((img_xpos, img_ypos)))

    def draw_screen(self, window):
        self.tiles.draw(window)
        self.tiles.update()

if __name__ == "__main__":
    config = GameConfig()
    config.set_config_val("window_size", (400, 400))
    model = GameModel()
    screen = ExplorableScreen(config, model)
    loop_events = GameLoopEvents(config, screen)
    loop = GameLoop(loop_events)
    loop.go()
