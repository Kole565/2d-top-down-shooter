import pygame

from bin.modules.moveable import Moveable


class Bullet(pygame.sprite.Sprite, Moveable):

    def __init__(self, cfg, field_size, direction, spawn_pos=[0, 0]):
        super().__init__()
        Moveable.init(self, spawn_pos)

        self.image = pygame.Surface([cfg["radius"] * 2, cfg["radius"] * 2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.circle(
            self.image, cfg["color"], [cfg["radius"], cfg["radius"]],
            cfg["radius"]
        )

        self.damage = cfg["damage"]
        self.piercing = cfg["piercing"]
        self.piercing_mod = cfg["piercing_damage_mod"]
        self.radius = cfg["radius"]
        self.side = cfg["side"]
        self.speed = cfg["projectile_speed"]

        self.field_size = field_size
        self.direction = direction

        self.collided_sprites = []

        self.group = "projectile"

    def update(self, *args, **kwargs):
        self.move(*self.direction, time_delta=kwargs["time_delta"])
        self.check_bounds()

    def on_collision(self, collisions):
        for sprite in collisions:
            if sprite.group == "obstacle":
                self.kill()
            elif sprite.group == "enemy" and self.group == "player_projectile":
                sprite.hit(self.damage)

                if self.piercing > 0:
                    self.piercing -= 1
                    self.damage *= self.piercing_mod
                else:
                    self.kill()
            elif sprite.group == "player" and self.group == "projectile":
                sprite.hit(self.damage)

                if self.piercing > 0:
                    self.piercing -= 1
                    self.damage *= self.piercing_mod
                else:
                    self.kill()

    def check_bounds(self):
        """Check out of bounds case."""
        if any((
            self.x <= -self.radius * 2,
            self.x >= self.field_size[0] + self.radius * 2,
            self.y <= -self.radius * 2,
            self.y >= self.field_size[1] + self.radius * 2,
        )):
            self.kill()
