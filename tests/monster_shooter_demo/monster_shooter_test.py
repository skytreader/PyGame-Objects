#! usr/bin/env python

from ...components.core import Colors
from ...components.core import GameLoopEvents
from ...components.core import GameConfig
from ...components.core import GameLoop
from ...components.core import GameScreen

from ...components.framework_exceptions import InstanceException

from ...components.image import Image

from ...components.shapes import Point

from sprites import Zombie, Shooter, Bullet

import os

import pygame

import random

"""
A shooting game inspired by Plants vs Zombies.

@author Chad Estioco
"""

class PVZMainScreen(GameScreen):
    
    def __init__(self, screen_dimensions):
        super(PVZMainScreen, self).__init__(screen_dimensions)
        self.__monster_sprite_group = pygame.sprite.Group()
        self.__player_sprite_group = pygame.sprite.Group()
        self.__bullet_sprite_group = pygame.sprite.Group()
        self.__score = 0
        self.__end_game = False
    
    @property
    def end_game(self):
        return self.__end_game
    
    @end_game.setter
    def end_game(self, is_end):
        self.__end_game = is_end
    
    @property
    def bullet_sprite_group(self):
        return self.__bullet_sprite_group
    
    @property
    def monster_sprite_group(self):
        return self.__monster_sprite_group
    
    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self, s):
        self.__score = s
    
    @property
    def player_sprite_group(self):
        return self.__player_sprite_group
    
    @property
    def meteormon(self):
        return self.__meteormon_sprite
    
    @property
    def bakemon(self):
        return self.__bakemon_sprite
    
    @property
    def monster_list(self):
        return self.__monster_list
    
    @property
    def shooter_sprite(self):
        return self.__shooter_sprite
    
    def shoot(self, event):
        # Initialize the bullet sprite
        shooter_xpos = self.shooter_sprite.rect.x
        shooter_width = self.shooter_sprite.screen_draw.width
        bullet = Bullet(shooter_width, self.shooter_sprite.rect.y + 39)
        self.bullet_sprite_group.add(bullet)
    
    # TODO Must be able to vary monster properties (Factory pattern at last?!)
    def setup(self):
        super(PVZMainScreen, self).setup()
        # Preload monster sprites
        meteormon_img = os.path.join("PyGame_Objects", "sample_sprites", "meteormon_clueless.png")
        bakemon_img = os.path.join("PyGame_Objects", "sample_sprites", "bakemon_attack.png")
        lalamon_img = os.path.join("PyGame_Objects", "sample_sprites", "lalamon_clueless.png")
        tentacly_img = os.path.join("PyGame_Objects", "sample_sprites", "tentacly_angry.png")
        self.__monster_list = [meteormon_img, bakemon_img, lalamon_img, tentacly_img]
        
        # Load the character sprite
        shooter_image = Image(os.path.join("PyGame_Objects","sample_sprites","seahomon_hero.png"))
        shooter_image.flip(True, False)
        
        shooter_image.position = Point(0, super(PVZMainScreen, self).screen_size[GameConfig.HEIGHT_INDEX] / 2)
        
        self.__shooter_sprite = Shooter(7, shooter_image, 10, self.screen_size[GameConfig.WIDTH_INDEX])
        self.player_sprite_group.add(self.shooter_sprite)
    
    def add_monster(self, monster):
        monster_image = Image(monster)
        screen_width = self.screen_size[GameConfig.WIDTH_INDEX]
        init_x = random.randint(screen_width, screen_width + 50)
        init_y = random.randint(0, self.screen_size[GameConfig.HEIGHT_INDEX] - 50)
        monster_image.position = Point(init_x, init_y)
        
        sprite = Zombie(5, monster_image, 10)
        
        self.monster_sprite_group.add(sprite)
    
    def draw_screen(self, window):
        if self.end_game:
            font = pygame.font.Font(None, 25)
            end_message = font.render("GAME OVER", True, Colors.RED)
            window.blit(end_message, [100, 100])
            return
        
        self.monster_sprite_group.draw(window)
        self.player_sprite_group.draw(window)
        self.bullet_sprite_group.draw(window)
        
        self.monster_sprite_group.update()
        self.player_sprite_group.update()
        self.bullet_sprite_group.update()
        
        font = pygame.font.Font(None, 25)
        score = font.render("Score: " + str(self.score), True, Colors.RED)
        window.blit(score, [100, 100])

class PVZEvents(GameLoopEvents):
    
    def __init__(self, config, game_screen):
        super(PVZEvents, self).__init__(config, game_screen)
        self.__meteormon = None
    
    def loop_event(self):
        self.window.fill(Colors.WHITE)
        
        if random.random() <= 0.3:
            monster_index = random.randint(0, len(self.game_screen.monster_list) - 1)
            self.game_screen.add_monster(self.game_screen.monster_list[monster_index])
        
        super(PVZEvents, self).loop_event()
        bullet_hits = pygame.sprite.groupcollide(self.game_screen.bullet_sprite_group, \
            self.game_screen.monster_sprite_group, True, True)
        
        self.game_screen.score += len(bullet_hits)
        
        self_hits = pygame.sprite.spritecollide(self.game_screen.shooter_sprite, \
            self.game_screen.monster_sprite_group, True)
        
        self.game_screen.score -= len(self_hits)
        
        self.game_screen.end_game = self.game_screen.score < 0
    
    def move_shooter(self, event):
        if event.key == pygame.K_UP:
            is_up = True
        elif event.key == pygame.K_DOWN:
            is_up = False
        
        super(PVZEvents, self).game_screen.shooter_sprite.is_going_up = is_up
        super(PVZEvents, self).game_screen.shooter_sprite.move()
        
    def loop_setup(self):
        super(PVZEvents, self).loop_setup()
        pygame.key.set_repeat(self.config.clock_rate, self.config.clock_rate)
    
    def attach_event_handlers(self):
        keydown_event = pygame.event.Event(pygame.KEYDOWN)
        
        up_dict = {}
        up_dict[GameLoopEvents.KEYCODE] = pygame.K_UP
        up_dict[GameLoopEvents.HANDLER] = self.move_shooter
        
        down_dict = {}
        down_dict[GameLoopEvents.KEYCODE] = pygame.K_DOWN
        down_dict[GameLoopEvents.HANDLER] = self.move_shooter
        
        shoot_dict = {}
        shoot_dict[GameLoopEvents.KEYCODE] = pygame.K_RETURN
        shoot_dict[GameLoopEvents.HANDLER] = self.game_screen.shoot
        
        self.add_event_handler(keydown_event, up_dict)
        self.add_event_handler(keydown_event, down_dict)
        self.add_event_handler(keydown_event, shoot_dict)
        
class PVZLoop(GameLoop):
    
    def __init__(self, events):
        """
        FIXME: Is this Pythonic enough?
        
        @param events
          Must be an instance of PVZEvents.
        """
        if isinstance(events, PVZEvents):
            super(PVZLoop, self).__init__(events)
        else:
            raise TypeError("PVZLoop expects an instance of PVZEvents")
    

config = GameConfig()
config.window_size = [500, 500]
config.clock_rate = 12
config.window_title = "PvZ Clone Demo"

screen = PVZMainScreen(config.window_size)

image_gle = PVZEvents(config, screen)
gl = PVZLoop(image_gle)
gl.go()
