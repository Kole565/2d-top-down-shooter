class AnimateObject:

    def move(self, rel_x, rel_y, mod=None, time_delta=1):
        """Change obj coordinate by float variables for bigger preciosness."""
        mult = self.speed if mod is None else mod
        self.x += rel_x * mult * time_delta
        self.y += rel_y * mult * time_delta

        self.rect.x = self.x
        self.rect.y = self.y

    def move_struct(self, rel_x, rel_y, mod=None, time_delta=1):
        """Change obj coordinate within borders."""
        mult = self.speed if mod is None else mod
        if any((
            self.x + rel_x * mult * time_delta < 0, 
            self.x + rel_x * mult * time_delta > self.field_size[0] - self.radius * 2,
            self.y + rel_y * mult * time_delta < 0,
            self.y + rel_y * mult * time_delta > self.field_size[1] - self.radius * 2
        )):
            return

        self.move(rel_x, rel_y, mod, time_delta=time_delta)
