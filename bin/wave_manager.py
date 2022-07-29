import pygame
from pygame_gui.elements import UILabel
import time
import random

from .entity.enemy.enemy import Enemy
from .entity.enemy.shooter import Shooter
from .entity.enemy.cami_enemy import CamiEnemy
from .utils import get_cfg
from .events import *


class WaveManger:

    """Implement waves system - 'enemy' attack during wave, break between waves for upgrading player."""

    def __init__(self, cfg, group, ui_handler, leveling, field_size, player):
        self.group = group
        self.ui_handler = ui_handler
        self.leveling = leveling
        self.field_size = field_size
        self.player = player
        
        self.waves = cfg["waves"]
        if cfg["spawn_position"] == "random":
            self.spawn_position = lambda: [random.randint(0, field_size[0]), random.randint(0, field_size[1])]
        else:
            self.spawn_position = lambda: [*cfg["spawn_position"]]

        self.classes = {
            "standart": [Enemy, get_cfg("enemy")["standart"]],
            "standart_shooter": [Shooter, get_cfg("enemy")["standart_shooter"]],
            "standart_cami": [CamiEnemy, get_cfg("enemy")["standart_cami"]],
        }
        
        self.wave_ind = 0
        self.is_wave = False
        self.is_active = False
        self.max_active_enemy = cfg["max_active_enemy"]

        self.queue = []
    
        self.wave_indicator = self.ui_handler.add(
            "is_wave_label", UILabel, ["top", "mid"],
            text="{}".format("Wave" if self.is_wave else "Break"),
            class_id="@default_label"
        )
        self.wave_counter = self.ui_handler.add (
            "wave_counter_label", UILabel, ["top", "mid"],
            text="Wave: {}".format(self.wave_ind+1),
            class_id="@default_label"
        )
        self.counter = self.ui_handler.add (
            "counter_label", UILabel, ["top", "mid"],
            text="Remain: {} s".format(0),
            class_id="@default_label"
        )
    
    def start(self):
        self.wave_ind = 0
        self.is_active = True
        self.last_wave_time = time.time()
        self.last_break_time = time.time()
        self.last_wave = False
        
    def update(self, *args, **kwargs):
        self.spawning()
        if not self.is_active:
            return

        self.check_wave()
        try:
            before_wave = self.waves[self.wave_ind]["duration"] - time.time() + self.last_wave_time
            before_break = self.waves[self.wave_ind]["break"] - time.time() + self.last_break_time
        except IndexError:
            return
        
        before_wave = 0 if before_wave < 0 else before_wave
        before_break = 0 if before_break < 0 else before_break

        self.wave_indicator.set_text("{}".format("Wave" if self.is_wave else "Break"))
        self.counter.set_text(
            "Remain: {:.0f} s".format(before_wave if self.is_wave else before_break)
        )
    
    def check_wave(self):
        try:
            wave = self.waves[self.wave_ind]
        except IndexError:
            self.is_active = False
            self.last_wave = True
            return

        if not self.is_wave and time.time() > self.last_break_time + wave["break"]:
            # Break ended, wave started case
            self.last_wave_time = time.time()
            self.is_wave = True
            self.start_wave()

        elif self.is_wave and time.time() > self.last_wave_time + wave["duration"] and not self.group:
            # Wave ended, break started case
            self.last_break_time = time.time()
            self.is_wave = False
            self.wave_ind += 1

        self.wave_counter.set_text("Wave: {}".format(self.wave_ind+1))
        
    def start_wave(self):
        wave = self.waves[self.wave_ind]

        entity = wave["entity"]
        for name, amount in entity.items():
            self.queue.append([*self.classes[name], amount])
    
    def spawning(self):
        """Create enemy instance if enemies amount less then perfomance limit.
        Post event when waves and enemies in them end.
        Use queue for delayed spawn.
        """
        if not self.queue or len(self.group) > self.max_active_enemy:
            if self.last_wave and not len(self.group):
                pygame.event.post(WAVES_ENDED)
            return

        while self.queue and len(self.group) <= self.max_active_enemy:
            if not self.queue[0][-1]:
                self.queue.pop(0)
                continue
            self.spawn(*self.queue[0])
            self.queue[0][-1] -= 1
    
    def spawn(self, obj_class, obj_cfg, amount=None):
        instance = obj_class(
            obj_cfg, self.ui_handler, self.leveling, self.field_size,
            self.player, self.spawn_position()
        )

        self.group.add(instance)
