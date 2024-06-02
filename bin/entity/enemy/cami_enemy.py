import pygame

from .enemy import Enemy
from bin.explosion import Explosion


class CamiEnemy(Enemy):

    def on_collision(self, collisions):
        super().on_collision(collisions)

        for sprite in collisions:
            if sprite.group == "player":
                sprite.hit(self.damage)

                expl = Explosion(self)
                self.group_for_markers.add(expl)

                self.kill()
