import pygame
from pygame_gui.elements import UIProgressBar, UILabel, UIPanel

from .powerup import Powerup, PowerupInfo
from .utils import get_cfg
from .exceptions import *


class Leveling:
    
    def __init__(self, screen, ui_handler, specks):
        self.specks = specks
        
        self.exp = 0
        self.level = 1
        self.next_level_exp = 25
        self.next_level_mod = 1.5
        self.skillpoints = 1

        self.level_label = ui_handler.add(
            "level_label", UILabel, ["top", "right"],
            text="{:2} level".format(self.level), class_id="@default_label"
        )
        self.exp_bar = ui_handler.add("exp_bar", UIProgressBar, ["top", "right"])
        self.skillpoints_label = ui_handler.add(
            "skillpoints_label", UILabel, ["bottom", "left"],
            text="{:2} skillpoints".format(self.skillpoints), class_id="@default_label"
        )
    
        self.powerups = [
            Powerup(
                get_cfg("ui")["powerup_1"], "powerup_1", ui_handler,
                PowerupInfo(pygame.K_1, self.specks, "player_shooting", "damage", 1.5, "*"),
                self
            ),
            Powerup(
                get_cfg("ui")["powerup_2"], "powerup_2", ui_handler,
                PowerupInfo(pygame.K_2, self.specks, "player_shooting", "rate", 1.5, "*"),
                self
            ),
            Powerup(
                get_cfg("ui")["powerup_3"], "powerup_3", ui_handler,
                PowerupInfo(pygame.K_3, self.specks, "player_shooting", "piercing", 1, "+"),
                self
            ),
            Powerup(
                get_cfg("ui")["powerup_4"], "powerup_4", ui_handler,
                PowerupInfo(pygame.K_4, self.specks, "player_shooting", "radius", 1.2, "*"),
                self
            ),
            Powerup(
                get_cfg("ui")["powerup_5"], "powerup_5", ui_handler,
                PowerupInfo(pygame.K_5, self.specks, "player", "health", 1.2, "*"),
                self
            ),
            Powerup(
                get_cfg("ui")["powerup_6"], "powerup_6", ui_handler,
                PowerupInfo(pygame.K_6, self.specks, "player", "speed", 1.1, "*"),
                self
            )
        ]

    def update(self, *args, **kwargs):
        self.powerups_update(*args, **kwargs)
    
    def powerups_update(self, *args, **kwargs):
        for powerup in self.powerups:
            powerup.update(*args, **kwargs)
    
    def enought_skillpoints_check(self):
        if self.skillpoints >= 1:
            return True
    
    def dec_skillpoint(self):
        if self.skillpoints < 1:
            raise NotEnoughtSkillpointsError

        self.skillpoints -= 1
        self.ui_update()
    
    def add(self, exp):
        self.exp += exp
        while self.exp >= self.next_level_exp:
            self.exp -= self.next_level_exp
            self.level_up()
        
        self.exp_bar.set_current_progress(self.exp / self.next_level_exp * 100)

    def level_up(self):
        self.level += 1
        self.next_level_exp *= self.next_level_mod
        self.skillpoints += 1

        self.exp_bar.set_current_progress(0)
        self.ui_update()
    
    def ui_update(self):
        self.level_label.set_text("{:2} level".format(self.level))
        self.skillpoints_label.set_text("{:2} skillpoints".format(self.skillpoints))
