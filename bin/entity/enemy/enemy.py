import pygame
from pygame_gui.elements import UIWorldSpaceHealthBar

from bin.modules.moveable import Moveable


class Enemy(pygame.sprite.Sprite, Moveable):

    aim_group = "player"

    def __init__(self, cfg, ui_handler, score, field_size, player, spawn_pos=[0, 0]):
        super().__init__()
        Moveable.init(self, spawn_pos)

        self.radius = cfg["radius"]
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, cfg["color"], [self.radius, self.radius], self.radius)

        self.speed = cfg["speed"]
        self.damage = cfg["damage"]
        self.exp = cfg["exp"]
        self.current_health = cfg["health"]
        self.health_capacity = cfg["health"]
        self.group = "enemy"

        self.ui_handler = ui_handler
        self.score = score
        self.field_size = field_size

        self.health_bar = self.ui_handler.add(
            "enemy_health_bar", UIWorldSpaceHealthBar, None,
            sprite_to_monitor=self
        )
        self.health_bar.follow_sprite_offset = -cfg["radius"] * 1.5, -cfg["radius"] * 2

        self.x, self.y = spawn_pos
        self.last_pos = spawn_pos
        self.aim = player

    def update(self, *args, **kwargs):
        self.moving(kwargs["time_delta"])

    def moving(self, time_delta):
        direction = self.get_direction(self.aim)

        self.move(*self.direction, time_delta=time_delta)

    def get_direction(self, aim):
        delta_x = aim.rect.x - self.rect.x
        delta_y = aim.rect.y - self.rect.y

        if delta_x == delta_y == 0:
            x = y = 0

        elif delta_x == 0:
            x = 0
            y = 1 if delta_y > 0 else -1
        elif delta_y == 0:
            x = 1 if delta_x > 0 else -1
            y = 0

        elif abs(delta_x) > abs(delta_y):
            x = 1 if delta_x > 0 else -1
            y = abs(delta_y / delta_x) if delta_y > 0 else -(abs(delta_y / delta_x))
        else:
            x = abs(delta_x / delta_y) if delta_x > 0 else -(abs(delta_x / delta_y))
            y = 1 if delta_y > 0 else -1

        self.direction = [x, y]
        return [x, y]

    def shoot(self):
        pass

    def hit(self, dmg):
        self.current_health -= dmg

        if self.current_health <= 0:
            self.kill()

    def kill(self):
        self.score.add(self.exp)
        self.health_bar.kill()
        super().kill()

    def on_collision(self, collisions):
        for sprite in collisions:
            if sprite.group == "obstacle":
                self.revert_pos()
