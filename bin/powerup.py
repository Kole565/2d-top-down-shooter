import pygame
from pygame_gui.elements import UIImage, UIButton

from .events import powerup_button_click
from .exceptions import NotEnoughtSkillpointsError


class PowerupInfo:

    def __init__(self, key, specks, parent, name, value, type):
        self.key = key
        self.specks = specks
        self.speck_parent = parent
        self.speck_name = name
        self.value = value
        self.type = type

class Powerup:

    def __init__(self, cfg, name, ui_handler, specks, leveling, **kwargs):
        side = None if "container" in kwargs else ["bottom", "left"]
        self.button = ui_handler.add(
            name, UIButton, side,
            text="", class_id="@powerup",
            starting_height=10,
            **kwargs
        )

        self.key = specks.key
        self.specks = specks.specks
        self.speck_parent = specks.speck_parent
        self.speck_name = specks.speck_name
        self.value = specks.value
        self.type = specks.type

        self.leveling = leveling
    
    def update(self, *args, **kwargs):
        self.button.update(kwargs["time_delta"])

        if not self.check() or not self.leveling.enought_skillpoints_check():
            return
        
        {
            "+": lambda: self.specks[self.speck_parent].add(self.speck_name, self.value),
            "-": lambda: self.specks[self.speck_parent].add(self.speck_name, -self.value),
            "*": lambda: self.specks[self.speck_parent].multiply(self.speck_name, self.value),
            "/": lambda: self.specks[self.speck_parent].multiply(self.speck_name, -self.value),
        }[self.type]()

        try:
            self.leveling.dec_skillpoint()
        except NotEnoughtSkillpointsError:
            pass

    def check(self):
        keys = pygame.key.get_pressed()
        if keys[self.key] or self.button.check_pressed():
            return True
    
    