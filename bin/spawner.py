import random
import time


class Spawner:

    def __init__(self, cfg, obj_cfg, obj_class, group, ui_handler, limits, score):
        self.spawn_speed = cfg["spawn_speed"]

        if cfg["spawn_position"] == "random":
            self.spawn_position = lambda: [random.randint(0, limits[0]), random.randint(0, limits[1])]
        else:
            self.spawn_position = lambda: [*cfg["spawn_position"]]

        self.obj_cfg = obj_cfg
        self.obj_class = obj_class
        self.group = group
        self.ui_handler = ui_handler
        self.field_size = limits
        self.score = score

        self.last_spawn = time.time()

    def update(self, *args, **kwargs):
        if not self.can_spawn():
            return

        instance = self.obj_class(
            self.obj_cfg, self.ui_handler, self.score, self.field_size, spawn_pos=self.spawn_position()
        )

        self.group.add(instance)

    def can_spawn(self):
        if self.spawn_speed == 0:
            return

        if time.time() - 10 / self.spawn_speed > self.last_spawn:
            self.last_spawn = time.time()
            return True
