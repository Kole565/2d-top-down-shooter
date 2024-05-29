import time

from .enemy import Enemy

from ..bullet import Bullet


class Shooter(Enemy):

    def __init__(self, cfg, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)

        self.bullets_group = kwargs["bullets_group"]

        self.shooting_cfg = cfg["shooting"]
        self.min_dist = self.shooting_cfg["min_dist"]
        self.last_shoot = time.time() - 1000

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        self.shooting()

    def shooting(self):
        direction = self.get_direction([self.aim.x, self.aim.y])
        self.shoot(direction)

    def shoot(self, direction):
        if not self.can_shoot():
            return

        projectile = Bullet(
            self.shooting_cfg,
            self.field_size,
            direction,
            [self.x + self.radius / 2, self.y + self.radius / 2]
        )

        self.bullets_group.add(projectile)

    def can_shoot(self):
        if self.shooting_cfg["rate"] == 0:
            return
        if time.time() > self.last_shoot + 10 / self.shooting_cfg["rate"]:
            self.last_shoot = time.time()
            return True
