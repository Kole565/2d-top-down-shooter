import time
import math

from .enemy import Enemy

from ..bullet import Bullet


class Shooter(Enemy):

    def __init__(self, cfg, *args, **kwargs):
        super().__init__(cfg, *args, **kwargs)

        self.shooting_cfg = cfg["shooting"]
        self.min_dist = self.shooting_cfg["min_dist"]
        self.last_shoot = time.time() - 1000
    
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        self.shooting(kwargs["groups"])
    
    def moving(self, time_delta):
        if math.dist((self.x, self.y), (self.aim.x, self.aim.y)) > self.min_dist:
            super().moving(time_delta)

    def shooting(self, groups):            
        direction = self.get_direction(self.aim)
        self.shoot(direction, groups["projectile"])
    
    def shoot(self, direction, group):
        if not self.can_shoot():
            return
        
        projectile = Bullet(
            self.shooting_cfg,
            self.field_size,
            direction,
            [self.x + self.radius/2, self.y + self.radius/2]
        )

        group.add(projectile)
    
    def can_shoot(self):
        if self.shooting_cfg["rate"] == 0:
            return
        if time.time() > self.last_shoot + 10/self.shooting_cfg["rate"]:
            self.last_shoot = time.time()
            return True
