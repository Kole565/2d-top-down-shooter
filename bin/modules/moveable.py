"""Provide Moveable class."""
from collections import deque


class Moveable:
    """Provide coordinates system."""

    @staticmethod
    def init(self, spawn_pos=[0, 0]):
        """Initialize position history."""
        self.x, self.y = spawn_pos

        self.last_positions = deque([spawn_pos], maxlen=4)

    def move_struct(self, rel_x, rel_y, mod=1, time_delta=1):
        """Change obj coordinate within borders."""
        abs_x = rel_x * self.speed * mod * time_delta
        abs_y = rel_y * self.speed * mod * time_delta
        if any((
            self.x + abs_x < 0,
            self.x + abs_x > self.field_size[0] - self.radius * 2,
            self.y + abs_y < 0,
            self.y + abs_y > self.field_size[1] - self.radius * 2
        )):
            return

        self.move(rel_x, rel_y, mod, time_delta=time_delta)

    def move(self, rel_x, rel_y, mod=1, time_delta=1):
        """Change obj coordinate by float variables for bigger preciosness."""
        self.last_positions.append([self.x, self.y])

        self.x += rel_x * self.speed * mod * time_delta
        self.y += rel_y * self.speed * mod * time_delta

        self.rect.x = self.x
        self.rect.y = self.y

    def revert_pos(self):
        """Restore previous position (e.g. for colision reaction)."""
        self.x, self.y = self.last_positions[0]
