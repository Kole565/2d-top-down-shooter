import pygame

from .animate_object import AnimateObject

from ..explosion import Explosion


class Bullet(pygame.sprite.Sprite, AnimateObject):

    def __init__(self, cfg, field_size, direction, spawn_pos=[0, 0]):
        super().__init__()
        
        self.image = pygame.Surface([cfg["radius"]*2, cfg["radius"]*2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, cfg["color"], [cfg["radius"], cfg["radius"]], cfg["radius"])
    
        self.damage = cfg["damage"]
        self.piercing = cfg["piercing"]
        self.piercing_mod = cfg["piercing_damage_mod"]
        self.radius = cfg["radius"]
        self.side = cfg["side"]
        self.speed = cfg["projectile_speed"]

        self.field_size = field_size
        self.direction = direction

        self.x, self.y = spawn_pos
        self.collided_sprites = []

    def update(self, groups, *args, **kwargs):
        self.move(*self.direction, time_delta=kwargs["time_delta"])
        self.check_collision(groups)
        self.check_bounds()
    
    def check_collision(self, groups):
        if self.side == "neutral":
            return
        group = groups["enemy"] if self.side == "friendly" else groups["player"]
        
        collision = pygame.sprite.spritecollide(self, group, False)
        if not collision:
            return

        for sprite in collision:
            if sprite in self.collided_sprites:
                continue
            self.collided_sprites.append(sprite)

            try:
                sprite.hit(self.damage)
            except AttributeError:
                pass
            
            e = Explosion(self)
            groups["projectile"].add(e)
            if not self.piercing:
                self.kill()
            else:
                self.piercing -= 1
                self.damage *= self.piercing_mod
    
    def check_bounds(self):
        """Check out of bounds case."""
        if any((
            self.x <= -self.radius*2,
            self.x >= self.field_size[0] + self.radius*2,
            self.y <= -self.radius*2,
            self.y >= self.field_size[1] + self.radius*2,
        )):
            self.kill()
