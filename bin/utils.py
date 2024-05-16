import pygame
from pygame_gui.elements import UILabel
import json
import os


def get_cfg(name):
    cfg = json.load(open(os.path.join(os.path.dirname(__file__), "../config", name + ".json")))

    return cfg

def get_image(filename):
    image = pygame.image.load(os.path.join(os.path.dirname(__file__), "../resources", "image", filename))

    return image


class FPSMeter:

    preciseness = 3

    def __init__(self, ui_handler):
        self.frames = [60 for i in range(self.preciseness)]

        self.fps_label = ui_handler.add(
            "fps_label", UILabel, ["bottom", "right"],
            text="{:}".format("NaN"), class_id="@default_label"
        )

    def update(self):
        self.fps_label.set_text("FPS: {:}".format(self.fps))

    @property
    def fps(self):
        return "{:.1f}".format(sum(self.frames) / len(self.frames))

    def add(self, value):
        self.frames = self.frames[1:] + [value]
