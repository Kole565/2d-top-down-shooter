"""Provide implementation of ObstacleManager class."""
from bin.entity.wall import Wall


class ObstaclesManager:
    """Manage obstacles on grid."""

    def __init__(self, cfg, obstacles_group, field_size):
        """Initialize obstacles on grid."""
        self.obstacles_group = obstacles_group

        self.wall_cfg = cfg["wall"]
        self.wall_grid = cfg["wall"]["grid"]
        self.wall_size = cfg["wall"]["size"]

        self.field_size = [field_size[0] * 1.1, field_size[1] * 1.1]

        self.grid_size = [
            int(self.field_size[0] // self.wall_size),
            int(self.field_size[1] // self.wall_size)
        ]

        self.init_walls()

    def init_walls(self):
        """Initialize walls on grid."""
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                if self.wall_grid[y][x] == "0":
                    continue

                spawn_position = [x * self.wall_size, y * self.wall_size]

                wall = Wall(self.wall_cfg, spawn_position)

                self.obstacles_group.add(wall)

    def get_obstacle_of_type(self, obj_type):
        """Filter and return obstacles by type."""
        print("1. ObstaclesManager")
        filtered = [
            obj for obj in self.obstacles_group if isinstance(obj, obj_type)
        ]
        print("2. ObstaclesManager", filtered)
        print("3. ObstaclesManager", type(self.obstacles_group.sprites()[0]), obj_type, isinstance(self.obstacles_group.sprites()[0], obj_type))
        return filtered
