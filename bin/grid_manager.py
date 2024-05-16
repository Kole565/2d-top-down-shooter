from .entity.wall import Wall


class GridManager:
    """Implement field conversion to grid for pathfinding."""

    def __init__(self, cfg, group, ui_handler, field_size, player):
        self.group = group
        # self.ui_handler = ui_handler
        self.grid_size = cfg["grid_size"]
        self.field_size = [field_size[0] * 1.1, field_size[1] * 1.1] # For borders covering
        # self.player = player

        self.wall_size = cfg["wall"]["size"]
        self.grid_size[0] = int(self.field_size[0] // self.wall_size)
        self.grid_size[1] = int(self.field_size[1] // self.wall_size)
        print(self.grid_size)

        self.walls_grid = cfg["walls"]
        self.wall_cfg = cfg["wall"]

        self.init_grid()
        self.init_walls()

    def init_grid(self):
        self.grid = [[[None, None, None] for x in range(self.grid_size[0])] for y in range(self.grid_size[1])]
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                self.grid[y][x] = [x, y, None]

    def init_walls(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.walls_grid[y][x] == "0":
                    continue

                spawn_position = [
                    self.grid[y][x][0] * self.wall_size,
                    self.grid[y][x][1] * self.wall_size
                ]

                wall = Wall(
                    self.wall_cfg, spawn_position
                )

                self.grid[y][x][2] = wall
                self.group.add(wall)

    def update(self, *args, **kwargs):
        pass
