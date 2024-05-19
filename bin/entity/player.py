import pygame
from pygame_gui.elements import UIScreenSpaceHealthBar
import time

from bin.modules.moveable import Moveable
from bin.modules.collisionable import Collisionable
from .bullet import Bullet

from ..specks import Specks
from ..events import PLAYER_LOSE


class Player(pygame.sprite.Sprite, Moveable, Collisionable):

    def __init__(self, cfg, ui_handler, field_size, spawn_pos=[0, 0]):
        super().__init__()
        Moveable.init(self, spawn_pos)

        self.ui_handler = ui_handler
        self.field_size = field_size

        self.radius = cfg["radius"]
        self.image = pygame.Surface([cfg["radius"] * 2, cfg["radius"] * 2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, cfg["color"], [cfg["radius"], cfg["radius"]], cfg["radius"])

        self.mask = pygame.mask.from_surface(self.image)

        op = cfg["over_powered"]
        self.specks = Specks(cfg["specks_op"]) if op else Specks(cfg["specks"])
        self.shooting = Specks(cfg["shooting_op"]) if op else Specks(cfg["shooting"])

        self.current_health = self.health_capacity * 1
        self.side = "friendly"

        self.ui_handler.add(
            "player_health_bar", UIScreenSpaceHealthBar, ["top", "left"],
            sprite_to_monitor=self
        )

        self.x, self.y = spawn_pos
        self.positions = [spawn_pos]
        self.can_move = {"x": True, "-x": True, "y": True, "-y": True}
        self.last_shoot = time.time() - 1000

        self.move(0, 0)

        self.group = "player"

    @property
    def speed(self):
        return self.specks["speed"]

    @property
    def health_capacity(self):
        return self.specks["health"]

    @property
    def shooting_rate(self):
        return self.shooting["rate"]

    def update(self, groups, *args, **kwargs):
        self.positions.append([self.x, self.y])

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (self.can_move["-y"]):
            self.move_struct(0, -1, time_delta=kwargs["time_delta"])
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (self.can_move["y"]):
            self.move_struct(0, 1, time_delta=kwargs["time_delta"])
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (self.can_move["-x"]):
            self.move_struct(-1, 0, time_delta=kwargs["time_delta"])
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (self.can_move["x"]):
            self.move_struct(1, 0, time_delta=kwargs["time_delta"])

        if keys[pygame.K_SPACE]:
            self.shoot(groups)

    def shoot(self, groups):
        if not self.can_shoot():
            return

        direction = self.get_shoot_direction()
        projectile = Bullet(
            self.shooting,
            self.field_size,
            direction,
            [self.x - self.shooting["radius"] + self.radius, self.y - self.shooting["radius"] + self.radius]
        )
        projectile.group = "player_projectile"

        projectile.add(groups["projectile"])

    def get_shoot_direction(self):
        # TODO: Use math normalisation here
        aim = pygame.mouse.get_pos()

        delta_x = aim[0] - self.rect.centerx
        delta_y = aim[1] - self.rect.centery

        if delta_x == delta_y == 0:
            x = y = 1

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

        return [x, y]

    def can_shoot(self):
        if self.shooting_rate == 0:
            return
        if time.time() > self.last_shoot + 10 / self.shooting_rate:
            self.last_shoot = time.time()
            return True

    def hit(self, dmg):
        if self.current_health - dmg <= 0:
            self.current_health = 0
            self.kill()
        else:
            self.current_health -= dmg

    def heal(self, hp):
        self.current_health += hp
        if self.current_health > self.health_capacity:
            self.current_health = self.health_capacity

    def heal_percent(self, perc):
        self.heal(self.health_capacity * perc / 100)

    def kill(self):
        pygame.event.post(PLAYER_LOSE)
        super().kill()

    def on_collision(self, collisions):
        for sprite in collisions:
            if sprite.group == "enemy":
                self.hit(1)

            elif sprite.group == "pickup":
                self.heal(sprite.hitpoints)
                sprite.kill()

            elif sprite.group == "obstacle":
                self.x, self.y = self.positions[-2]
