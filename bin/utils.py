"""Provide various functions for different separeted in code tasks."""
import pygame
from pygame_gui.elements import UILabel
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


class Node:

    def __init__(self, position, steps=0, distance=0, parent=None):
        self.x = position[0]
        self.y = position[1]

        self.steps = steps
        self.distance = distance

        self.parent = parent

    @property
    def position(self):
        return [self.x, self.y]

    def __repr__(self):
        return "{} {}".format(*self.position)


def a_star(start, end, obstacles, borders, cell_size=1, seen=None):
    """Return path from start to end through field filled with obstacles."""
    start = Node(start)
    end = Node(end)
    if start.position == end.position:
        return None
    if end.position in obstacles:
        return None

    seen = [start.position]
    to_explore = get_valid_cells(
        start, end, seen, obstacles, borders, cell_size
    )

    while to_explore:
        node = to_explore.pop()

        if node.position == end.position:
            break
        if node.position in seen:
            continue

        seen.append(node.position)
        to_explore.extend(get_valid_cells(
            node, end, seen, obstacles, borders, cell_size
        ))

        to_explore.sort(key=lambda x: x.steps + x.distance, reverse=True)

    if not node:
        return None

    path = []
    while node:
        path.append(node.position)
        node = node.parent

    return path[::-1]


def get_valid_cells(start, end, seen, obstacles, borders, cell_size=1):
    """Return cells.

    Criterias: adjacent, wasn't met, not obstacle and within borders.
    """
    cells = []

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            if dx != 0 and dy != 0:
                continue

            pos = [start.x + dx * cell_size, start.y + dy * cell_size]
            next_cell = Node(
                pos, steps=start.steps + cell_size,
                distance=math.dist(pos, end.position),
                parent=start
            )

            if next_cell.position in seen:
                continue
            if (
                next_cell.x < 0 or next_cell.x >= borders[0]
                or next_cell.y < 0 or next_cell.y >= borders[1]
            ):
                continue
            if next_cell.position in obstacles:
                continue

            cells.append(next_cell)

    return cells
