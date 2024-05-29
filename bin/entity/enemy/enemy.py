"""Provide Enemy class."""
import heapq
import math
import pygame

from bin.entity.wall import Wall
from bin.modules.moveable import Moveable
from bin.entity.marker import Marker
from pygame_gui.elements import UIWorldSpaceHealthBar


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float("inf")  # Расстояние от начального узла до текущего узла
        self.h = 0  # Примерное расстояние от текущего узла до конечного узла
        self.f = float("inf")  # Сумма g и h
        self.parent = None  # Родительский узел, используется для восстановления пути

    # Переопределяем оператор сравнения для сравнения узлов
    def __lt__(self, other):
        return self.f < other.f

    # Переопределяем оператор равенства для сравнения узлов
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Enemy(pygame.sprite.Sprite, Moveable):

    aim_group = "player"

    def __init__(self, cfg, group, ui_handler, score, field_size, obstacles_manager, player, spawn_pos=[0, 0], *args, **kwargs):
        print("1. Enemy init")
        super().__init__()
        Moveable.init(self, spawn_pos)
        print("2. Enemy init")

        self.wall_size = 100
        self.group_for_markers = group
        print("2.1 Enemy init")

        self.radius = cfg["radius"]
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, cfg["color"], [self.radius, self.radius], self.radius)
        print("2.2 Enemy init")

        self.speed = cfg["speed"]
        self.damage = cfg["damage"]
        self.exp = cfg["exp"]
        self.current_health = cfg["health"]
        self.health_capacity = cfg["health"]
        self.group = "enemy"
        print("2.3 Enemy init")

        self.ui_handler = ui_handler
        self.score = score
        self.field_size = field_size
        print("2.4.1 Enemy init")
        walls = obstacles_manager.get_obstacle_of_type(Wall)
        print("Walls?:", walls)
        self.walls_abs = [[wall.rect.x, wall.rect.y] for wall in walls]
        print("2.4.2 Enemy init")
        self.health_bar = self.ui_handler.add(
            "enemy_health_bar", UIWorldSpaceHealthBar, None,
            sprite_to_monitor=self
        )
        self.health_bar.follow_sprite_offset = -cfg["radius"] * 1.5, -cfg["radius"] * 2
        print("2.5 Enemy init")
        self.x, self.y = spawn_pos
        self.rect.x, self.rect.y = spawn_pos
        self.aim = player
        print("2.6 Enemy init")

        self.markers = []
        self.ignored_waypoint = None

        print("3. Enemy init")

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
        ) < self.wall_size * 0.4:
            return [self.aim.x, self.aim.y]

        obstacles = self.walls_abs

        start_in_grid, end_in_grid = [None, None], [None, None]
        start_in_grid[0] = int(self.x // self.wall_size * self.wall_size)
        start_in_grid[1] = int(self.y // self.wall_size * self.wall_size)

        end_in_grid[0] = int(self.aim.x // self.wall_size * self.wall_size)
        end_in_grid[1] = int(self.aim.y // self.wall_size * self.wall_size)

        if start_in_grid in obstacles:
            self.kill()

        path = self._astar(start_in_grid, end_in_grid, obstacles, self.wall_size)
        if path:
            for cell in path:
                waypoint = [cell[0] + self.wall_size / 2, cell[1] + self.wall_size / 2]

                marker = Marker(waypoint)
                self.group_for_markers.add(marker)

            x, y = self.x, self.y
            wall_offset = self.wall_size / 2
            try:
                if [path[0][0] + wall_offset, path[0][1] + wall_offset] == self.ignored_waypoint:
                    waypoint = [path[1][0] + wall_offset, path[1][1] + wall_offset]
                else:
                    if math.dist([self.x, self.y], [path[0][0] + wall_offset, path[0][1] + wall_offset]) < self.wall_size * 0.3:
                        self.ignored_waypoint = [path[0][0] + wall_offset, path[0][1] + wall_offset]
                        waypoint = [path[1][0] + wall_offset, path[1][1] + wall_offset]
                    else:
                        waypoint = [path[0][0] + wall_offset, path[0][1] + wall_offset]
            except IndexError:
                return [self.aim.x, self.aim.y]

            return waypoint


    def _astar(self, start, end, obstacles, mod=1):
        # Create start and end nodes
        start_node = Node(start[0], start[1])
        start_node.g = 0
        start_node.f = start_node.g + start_node.h
        end_node = Node(end[0], end[1])

        open_list = []
        heapq.heappush(open_list, start_node)

        closed_set = set()

        while open_list:
            current_node = heapq.heappop(open_list)

            if current_node == end_node:
                path = []
                while current_node is not None:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]  # Return the reversed path

            closed_set.add(current_node)

            neighbors = []

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    # Ignore the current node
                    if dx == 0 and dy == 0:
                        continue
                    if dx != 0 and dy != 0:
                        continue

                    x = current_node.x + dx * mod
                    y = current_node.y + dy * mod

                    if x < 0 or x >= self.field_size[0] or y < 0 or y >= self.field_size[1]:
                        continue

                    if [int(x), int(y)] in obstacles:
                        continue

                    neighbor = Node(x, y)
                    neighbors.append(neighbor)

            for neighbor in neighbors:
                if neighbor in closed_set:
                    continue

                new_g = current_node.g + 1 * mod

                if neighbor in open_list:
                    if new_g < neighbor.g:
                        neighbor.g = new_g
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.parent = current_node
                        heapq.heapify(open_list)  # Re-heapify to maintain priority
                else:
                    neighbor.g = new_g
                    neighbor.h = math.sqrt((end_node.x - neighbor.x) ** 2 + (end_node.y - neighbor.y) ** 2)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node
                    heapq.heappush(open_list, neighbor)

        return None

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
            y = abs(delta_y / delta_x) if delta_y > 0 else -(abs(delta_y / delta_x))
        else:
            x = abs(delta_x / delta_y) if delta_x > 0 else -(abs(delta_x / delta_y))
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
