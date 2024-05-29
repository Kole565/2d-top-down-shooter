"""Provide Player class."""
import pygame
import time

from bin.entity.bullet import Bullet
from bin.events import PLAYER_LOSE
from bin.modules.moveable import Moveable
from bin.specks import Specks
from pygame_gui.elements import UIScreenSpaceHealthBar


class Player(pygame.sprite.Sprite, Moveable):
    """Main player class. Used in The Game."""

    def __init__(self, cfg, projectile_group, ui_handler, field_size, spawn_pos=[0, 0]):
        """Init main player and it's modules."""
        super().__init__()
        Moveable.init(self, spawn_pos)

        self.projectile_group = projectile_group
        self.ui_handler = ui_handler
        self.field_size = field_size

        self.radius = cfg["radius"]
        self.image = pygame.Surface([cfg["radius"] * 2, cfg["radius"] * 2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.circle(
            self.image, cfg["color"], [self.radius, self.radius], self.radius
        )

        if cfg["over_powered"]:
            self.specks = Specks(cfg["specks_op"])
            self.shooting = Specks(cfg["shooting_op"])
        else:
            self.specks = Specks(cfg["specks"])
            self.shooting = Specks(cfg["shooting"])

        self.current_health = self.health_capacity

        self.ui_handler.add(
            "player_health_bar", UIScreenSpaceHealthBar, ["top", "left"],
            sprite_to_monitor=self
        )

        self.last_shoot = time.time() - 1000

        self.move(0, 0)

        self.group = "player"

    @property
    def speed(self):
        """Incapsulate specks."""
        return self.specks["speed"]

    @property
    def health_capacity(self):
        """Incapsulate specks."""
        return self.specks["health"]

    @property
    def shooting_rate(self):
        """Incapsulate specks."""
        return self.shooting["rate"]

    def update(self, *args, **kwargs):
        """Provide player interaction."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move_struct(0, -1, time_delta=kwargs["time_delta"])
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move_struct(0, 1, time_delta=kwargs["time_delta"])
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.move_struct(-1, 0, time_delta=kwargs["time_delta"])
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.move_struct(1, 0, time_delta=kwargs["time_delta"])

        if keys[pygame.K_SPACE]:
            self._shoot()

    def _shoot(self):
        if not self._can_shoot():
            return

        direction = self._get_shoot_direction()
        position = [
            self.x - self.shooting["radius"] + self.radius,
            self.y - self.shooting["radius"] + self.radius
        ]
        projectile = Bullet(
            self.shooting,
            self.field_size,
            direction,
            position
        )
        projectile.group = "player_projectile"

        self.projectile_group.add(projectile)

    def _can_shoot(self):
        if self.shooting_rate == 0:
            return
        if time.time() > self.last_shoot + 10 / self.shooting_rate:
            self.last_shoot = time.time()
            return True

    def _get_shoot_direction(self):
        aim = pygame.mouse.get_pos()

        delta_x = aim[0] - self.rect.centerx
        delta_y = aim[1] - self.rect.centery

        if delta_x == delta_y == 0:
            x = y = 1  # Default

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

    def hit(self, dmg):
        """Decrease hp or kill."""
        if self.current_health - dmg <= 0:
            self.current_health = 0
            self.kill()
        else:
            self.current_health -= dmg

    def heal(self, hp):
        """Increase hp up to limit."""
        self.current_health += hp
        if self.current_health > self.health_capacity:
            self.current_health = self.health_capacity

    def heal_percent(self, perc):
        """Increase hp up to limit. In percent."""
        self.heal(self.health_capacity * perc / 100)

    def kill(self):
        """Handle player gameover."""
        pygame.event.post(PLAYER_LOSE)
        super().kill()

    def on_collision(self, collisions):
        """Handle collision by types."""
        for sprite in collisions:
            if sprite.group == "enemy":
                self.hit(sprite.damage)

            elif sprite.group == "pickup":
                self.heal(sprite.hitpoints)
                sprite.kill()

            elif sprite.group == "obstacle":
                self.revert_pos()
