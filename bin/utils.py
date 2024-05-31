"""Provide various functions for different separeted in code tasks."""
import pygame
from pygame_gui.elements import UILabel
import heapq
import math
import json
import os


class FPSMeter:
    """Manager for fps value."""

    preciseness = 3

    def __init__(self, ui_handler):
        """Initialize fps history and ui."""
        self.frames = [60 for i in range(self.preciseness)]

        self.fps_label = ui_handler.add(
            "fps_label", UILabel, ["bottom", "right"],
            text="{:}".format("NaN"), class_id="@default_label"
        )

    def update(self):
        """Update fps label."""
        self.fps_label.set_text("FPS: {:}".format(self.fps))

    @property
    def fps(self):
        """Return formatted fps."""
        return "{:.1f}".format(sum(self.frames) / len(self.frames))

    def add(self, value):
        """Append frames queue."""
        self.frames = self.frames[1:] + [value]


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def get_cfg(name):
    """Return config dict from dedicated folder."""
    cfg = json.load(open(os.path.join(
        os.path.dirname(__file__), "../config", name + ".json"
    )))

    return cfg


def get_image(filename):
    """Return image from dedicated folder."""
    image = pygame.image.load(os.path.join(
        os.path.dirname(__file__), "../resources", "image", filename
    ))

    return image


def a_star(start, end, obstacles, borders, cell_size=1):
    """Return path from start to end through field filled with obstacles."""
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

                x = current_node.x + dx * cell_size
                y = current_node.y + dy * cell_size

                if x < 0 or x >= borders[0] or y < 0 or y >= borders[1]:
                    continue

                if [int(x), int(y)] in obstacles:
                    continue

                neighbor = Node(x, y)
                neighbors.append(neighbor)

        for neighbor in neighbors:
            if neighbor in closed_set:
                continue

            new_g = current_node.g + 1 * cell_size

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
