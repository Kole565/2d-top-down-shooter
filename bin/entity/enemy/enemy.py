"""Provide Enemy class."""
import math
import pygame

from pygame_gui.elements import UIWorldSpaceHealthBar

from bin.entity.marker import Marker
from bin.entity.wall import Wall
from bin.modules.moveable import Moveable
from bin.utils import a_star


class Enemy(pygame.sprite.Sprite, Moveable):

    aim_group = "player"

    def __init__(self, cfg, group, ui_handler, score, field_size, obstacles_manager, player, spawn_pos=[0, 0], *args, **kwargs):
        super().__init__()
        Moveable.init(self, spawn_pos)

        self.wall_size = 100
        self.group_for_markers = group

        self.radius = cfg["radius"]
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, cfg["color"], [self.radius, self.radius], self.radius)

        self.speed = cfg["speed"]
        self.damage = cfg["damage"]
        self.exp = cfg["exp"]
        self.current_health = cfg["health"]
        self.health_capacity = cfg["health"]
        self.group = "enemy"

        self.ui_handler = ui_handler
        self.score = score
        self.field_size = field_size

        walls = obstacles_manager.get_obstacle_of_type(Wall)
        self.walls_abs = [[wall.rect.x, wall.rect.y] for wall in walls]

        self.health_bar = self.ui_handler.add(
            "enemy_health_bar", UIWorldSpaceHealthBar, None,
            sprite_to_monitor=self
        )
        self.health_bar.follow_sprite_offset = -cfg["radius"] * 1.5, -cfg["radius"] * 2

        self.x, self.y = spawn_pos
        self.rect.x, self.rect.y = spawn_pos
        self.aim = player

        self.path = []
        self.ignored_waypoint = None
        self.markers = []

    def update(self, *args, **kwargs):
        self.moving(kwargs["time_delta"])

    def moving(self, time_delta):
        waypoint = self.get_waypoint()
        if waypoint is None:
            return

        self.move(*self.get_direction(waypoint), time_delta=time_delta)

    def get_waypoint(self):
        if math.dist(
            [self.x, self.y], [self.aim.x, self.aim.y]
        ) < self.wall_size * 0.5:
            return [self.aim.x, self.aim.y]

        obstacles = self.walls_abs

        start_in_grid, end_in_grid = [None, None], [None, None]
        start_in_grid[0] = int(self.x // self.wall_size * self.wall_size)
        start_in_grid[1] = int(self.y // self.wall_size * self.wall_size)

        end_in_grid[0] = int(self.aim.x // self.wall_size * self.wall_size)
        end_in_grid[1] = int(self.aim.y // self.wall_size * self.wall_size)

        if start_in_grid in obstacles:
            self.kill()

        if not self.path or end_in_grid != self.path[-1]:
            new_path = a_star(
                start_in_grid, end_in_grid, obstacles, self.field_size,
                self.wall_size
            )
            if new_path:
                self.path = new_path

        if not self.path:
            return [self.aim.x, self.aim.y]

        self._show_markers_on_grid(self.path)

        offset = [self.wall_size / 2, self.wall_size / 2]
        waypoint = [self.path[0][0] + offset[0], self.path[0][1] + offset[1]]
        if waypoint == self.ignored_waypoint:
            waypoint = [
                self.path[1][0] + offset[0], self.path[1][1] + offset[1]
            ]
            self.path.pop(0)
        else:
            if math.dist(waypoint, [self.x, self.y]) < 0.3 * self.wall_size:
                self.path.pop(0)
                self.ignored_waypoint = waypoint[:]

        waypoint[0] += (self.aim.radius - self.radius) / 2
        waypoint[1] += (self.aim.radius - self.radius) / 2

        return waypoint

    def _show_markers_on_grid(self, positions):
        for pos in positions:
            offset = [self.wall_size / 2, self.wall_size / 2]
            marker_pos = [pos[0] + offset[0], pos[1] + offset[1]]

            marker = Marker(marker_pos)
            self.group_for_markers.add(marker)

    def get_direction(self, aim):
        delta_x = aim[0] - self.rect.x
        delta_y = aim[1] - self.rect.y

        if delta_x == delta_y == 0:
            x = y = 0

        elif delta_x == 0:
            x = 0
            y = 1 if delta_y > 0 else -1
        elif delta_y == 0:
            x = 1 if delta_x > 0 else -1
            y = 0

        elif abs(delta_x) > abs(delta_y):
            x = 1 if delta_x > 0 else -1
            y = abs(delta_y / delta_x)
            if delta_y < 0:
                y *= -1
        else:
            x = abs(delta_x / delta_y)
            if delta_x < 0:
                x *= -1
            y = 1 if delta_y > 0 else -1

        self.direction = [x, y]
        return [x, y]

    def shoot(self):
        pass

    def hit(self, dmg):
        self.current_health -= dmg

        if self.current_health <= 0:
            self.kill()

    def kill(self):
        self.score.add(self.exp)
        self.health_bar.kill()
        super().kill()

    def on_collision(self, collisions):
        for sprite in collisions:
            if sprite.group == "obstacle":
                self.revert_pos()
