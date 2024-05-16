import pygame
import pygame_gui

from pygame_gui.core import ObjectID

from .exceptions import *


class UIHandler:

    THEME = "./config/theme.json"
    INDENT = 5

    def __init__(self, cfg, screen):
        self.cfg = cfg
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.ui_manager = pygame_gui.ui_manager.UIManager(self.screen_size, theme_path=self.THEME)

        self.elements = {}
        self.reserved = {
            "center": -200,
            "top": {
                "left": 0,
                "mid": 0,
                "right": 0
            },
            "bottom": {
                "left": 0,
                "mid": 0,
                "right": 0
            }
        }

    def process_events(self, event):
        self.ui_manager.process_events(event)

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def draw(self):
        self.ui_manager.draw_ui(self.screen)

    def add(self, name, instance, side=None, class_id=None, **kwargs):
        """Shell method for easier mangement instances of ui elements.
        Return instance of ui element.
        """
        try:
            if "relative_size" in self.cfg[name]:
                size = [
                    self.cfg[name]["relative_size"][0] / 100 * self.screen_size[0],
                    self.cfg[name]["relative_size"][1] / 100 * self.screen_size[1]
                ]
            else:
                size = self.cfg[name]["size"]
        except KeyError:
            raise MissingConfigWarning(name)

        element = instance(
            relative_rect=pygame.Rect(self.get_position(side, size), (size)),
            manager=self.ui_manager,
            object_id=ObjectID(object_id="#{}".format(name), class_id=class_id),
            **kwargs
        )
        self.elements[name] = element

        return element

    def add_absolute(self, name, instance, relative_position, relative_size, class_id=None, **kwargs):
        position = [
            relative_position[0] / 100 * self.screen_size[0],
            relative_position[1] / 100 * self.screen_size[1]
        ]
        size = [
            relative_size[0] / 100 * self.screen_size[0],
            relative_size[1] / 100 * self.screen_size[1]
        ]

        element = instance(
            relative_rect=pygame.Rect(position, size), manager=self.ui_manager,
            object_id=ObjectID(object_id="#{}".format(name), class_id=class_id),
            **kwargs
        )
        self.elements[name] = element

        return element

    def remove(self, *names):
        for name in names:
            try:
                self.ui_manager.get_sprite_group().remove(self.elements[name])
                self.elements.pop(name)
                self.reserved["center"] = -200 # TODO: Others elements should be supported
            except KeyError:
                pass # TODO: Warn about this

    def get_position(self, side, size):
        if not side:
            return [0, 0]

        if side[0] == "center":
            position = [
                (self.screen_size[0] - size[0]) // 2,
                self.screen_size[1] // 2 + self.reserved["center"],
            ]
            self.reserved["center"] += self.INDENT + size[1]

        elif side[0] == "top":

            if side[1] == "left":
                position = [
                    self.INDENT,
                    self.INDENT + self.reserved["top"]["left"],
                ]
                self.reserved["top"]["left"] += self.INDENT + size[1]
            elif side[1] == "mid":
                position = [
                    (self.screen_size[0] - size[0]) / 2,
                    self.INDENT + self.reserved["top"]["mid"],
                ]
                self.reserved["top"]["mid"] += self.INDENT + size[1]
            elif side[1] == "right":
                position = [
                    self.screen_size[0] - self.INDENT - size[0],
                    self.INDENT + self.reserved["top"]["right"],
                ]
                self.reserved["top"]["right"] += self.INDENT + size[1]

        elif side[0] == "bottom":

            if side[1] == "left":
                position = [
                    self.INDENT + self.reserved["bottom"]["left"],
                    self.screen_size[1] - self.INDENT - size[1],
                ]
                self.reserved["bottom"]["left"] += self.INDENT + size[0]
            elif side[1] == "mid":
                pass
            elif side[1] == "right":
                position = [
                    self.screen_size[0] - self.INDENT - size[0],
                    self.screen_size[1] - self.INDENT - size[1] - self.reserved["bottom"]["right"],
                ]
                self.reserved["bottom"]["right"] += self.INDENT + size[1]

        elif side[0] == "left":

            if side[1] == "top":
                pass
            elif side[1] == "mid":
                pass
            elif side[1] == "bottom":
                pass

        elif side[0] == "right":

            if side[1] == "top":
                pass
            elif side[1] == "mid":
                pass
            elif side[1] == "bottom":
                pass

        return position
