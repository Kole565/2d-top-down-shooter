"""Provide various functions for different separeted in code tasks."""
import pygame
from pygame_gui.elements import UILabel
import math
import json
import os
from copy import copy


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


def a_star(start, end, obstacles, borders, cell_size=1, seen=None):
    """Return path from start to end through field filled with obstacles."""
    seen = [copy(start)]
    return _a_star_rec(
        start, end, obstacles, borders, seen, cell_size=cell_size
    )


def _a_star_rec(start, end, obstacles, borders, seen, cell_size=1):
    if start == end:
        return seen

    to_explore = _get_valid_cells(start, seen, obstacles, borders, cell_size)
    to_explore.sort(key=lambda x: math.dist(x, end))

    if not to_explore:
        return

    for node in to_explore:
        path = _a_star_rec(
            node, end, obstacles, borders, copy(seen + [node]),
            cell_size=cell_size
        )
        if path:
            return path


def _get_valid_cells(start, seen, obstacles, borders, cell_size=1):
    cells = []

    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            if dx != 0 and dy != 0:
                continue

            next_cell = [start[0] + dx * cell_size, start[1] + dy * cell_size]

            if next_cell in seen:
                continue
            if (
                next_cell[0] < 0 or next_cell[0] >= borders[0]
                or next_cell[1] < 0 or next_cell[1] >= borders[1]
            ):
                continue
            if next_cell in obstacles:
                continue

            cells.append(next_cell)

    return cells
