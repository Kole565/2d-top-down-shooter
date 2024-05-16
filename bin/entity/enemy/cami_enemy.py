import pygame

from .enemy import Enemy

from ...explosion import Explosion


class CamiEnemy(Enemy):

    def check_collision(self, groups, *args, **kwargs):
        collision = pygame.sprite.collide_circle(self, self.aim)
        if not collision:
            return

        self.aim.hit(self.damage)

        e = Explosion(self)
        groups["enemy"].add(e)

        self.kill()
