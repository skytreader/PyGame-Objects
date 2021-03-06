#! usr/bin/env python

from components.core import Colors, GameConfig, GameLoop, GameLoopEvents, GameModel, GameScreen
from components.image import Image
from components.shapes import Point

from .sprites import Zombie, Shooter, Bullet

import os

import pygame

import random

"""
A shooting game inspired by Plants vs Zombies.

@author Chad Estioco
"""

class PVZMainScreen(GameScreen):
    
    def __init__(self, config):
        super(PVZMainScreen, self).__init__(config, GameModel())
        self.monster_sprite_group = pygame.sprite.Group()
        self.player_sprite_group = pygame.sprite.Group()
        self.bullet_sprite_group = pygame.sprite.Group()
        self.score = 0
        self.end_game = False
    
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
        meteormon_img = os.path.join("sample_sprites", "notmine", "meteormon_clueless.png")
        bakemon_img = os.path.join("sample_sprites", "notmine", "bakemon_attack.png")
        lalamon_img = os.path.join("sample_sprites", "notmine", "lalamon_clueless.png")
        tentacly_img = os.path.join("sample_sprites", "notmine", "tentacly_angry.png")
        self.monster_list = [meteormon_img, bakemon_img, lalamon_img, tentacly_img]
        
        # Load the character sprite
        shooter_image = Image(os.path.join("sample_sprites", "notmine", "seahomon_hero.png"))
        shooter_image.flip(True, False)
        
        shooter_image.position = Point(0, super(PVZMainScreen, self).screen_size[GameConfig.HEIGHT_INDEX] / 2)
        
        self.shooter_sprite = Shooter(7, shooter_image, 10, self.screen_size[GameConfig.WIDTH_INDEX])
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
            end_message = font.render("GAME OVER", True, Colors.MAX_RED)
            window.blit(end_message, [100, 100])
            return
        
        self.monster_sprite_group.draw(window)
        self.player_sprite_group.draw(window)
        self.bullet_sprite_group.draw(window)
        
        self.monster_sprite_group.update()
        self.player_sprite_group.update()
        self.bullet_sprite_group.update()
        
        font = pygame.font.Font(None, 25)
        score = font.render("Score: " + str(self.score), True, Colors.MAX_RED)
        window.blit(score, [100, 100])

class PVZEvents(GameLoopEvents):
    
    def __init__(self, config, game_screen):
        super(PVZEvents, self).__init__(game_screen)
        self.__meteormon = None
        self.key_controls = GameLoopEvents.KeyControls()
        self.key_controls.register_key(
            pygame.K_UP,
            lambda event: self.game_screen.shooter_sprite.move(True)
        )
        self.key_controls.register_key(
            pygame.K_DOWN,
            lambda event: self.game_screen.shooter_sprite.move(False)
        )
        self.key_controls.register_key(
            pygame.K_RETURN,
            self.game_screen.shoot
        )
    
    def loop_event(self):
        self.window.fill(Colors.MAX_WHITE)
        
        if random.random() <= 0.3:
            monster = random.choice(self.game_screen.monster_list)
            self.game_screen.add_monster(monster)
        
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
        
        self.game_screen.shooter_sprite.is_going_up = is_up
        self.game_screen.shooter_sprite.move()
        
    def loop_setup(self):
        super(PVZEvents, self).loop_setup()
        clock_rate = self.config.get_config_val("clock_rate")
        pygame.key.set_repeat(clock_rate, clock_rate)
    
    def attach_event_handlers(self):
        keydown_event = pygame.event.Event(pygame.KEYDOWN)
        
        self.add_event_handler(keydown_event, self.key_controls.handle)

if __name__ == "__main__":
    config = GameConfig()
    config.set_config_val("window_size", [500, 500])
    config.set_config_val("clock_rate", 60)
    config.set_config_val("window_title", "PvZ Clone Demo")
    
    screen = PVZMainScreen(config)
    
    image_gle = PVZEvents(config, screen)
    gl = GameLoop(image_gle)
    gl.go()
