import pygame

from .exceptions import *


class Heal(pygame.sprite.Sprite):

    aim_group = "player"
    
    def __init__(self, cfg, ui_manager, score, field_size, spawn_pos=[0, 0]):
        super().__init__()

        self.image = pygame.Surface([cfg["radius"]*2, cfg["radius"]*2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, cfg["color"], [cfg["radius"], cfg["radius"]], cfg["radius"])

        self.hitpoints = cfg["hitpoints"]
        self.hitpoints_percent = cfg["hitpoints_percent"]
        self.side = "pickup"

        self.x, self.y = spawn_pos
        self.rect.x, self.rect.y = self.x, self.y
    
    def update(self, groups, *args, **kwargs):
        self.check_collision(groups[self.aim_group])
    
    def check_collision(self, group):
        collision = pygame.sprite.spritecollide(self, group, False)
        if not collision:
            return
        
        for sprite in collision:
            if sprite.side == "pickup":
                continue
            
            try:
                if sprite.health_capacity * self.hitpoints_percent < self.hitpoints:
                    sprite.heal(self.hitpoints)
                else:
                    sprite.heal_percent(self.hitpoints_percent)
            except FullHealth:
                return

            self.kill()
