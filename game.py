import pygame
import time
from pygame_gui.elements import UILabel

from bin.ui_handler import UIHandler
from bin.wave_manager import WaveManger
from bin.spawner import Spawner
from bin.tutorial import Tutorial
from bin.leveling import Leveling
from bin.entity.player import Player
from bin.heal import Heal
from bin.explosion import Explosion
from bin.utils import *
from bin.events import *


class Game:

    """2d top-down shooter game class. Very vaguely simular to Enter The Gungeon.
    
    For game operating used 'state' field with possible values as:
    prestarted - Before main game start. There can be instructions, story, boosts, etc.
    Not menu or other separated scenes for 'prestarted' state! It's only for game session prestart.
    running - Main game cycle state.
    win - When all enemies defeated and player alive.
    lose - When player defeated.
    end - Special state for disabling all mechanics.
    paused - Pause game or smth. (Not Implemented)

    For configurating use json files in 'config' folder:
    game - Global settings.
    waves - Set up some new waves, if want.
    P.S. set to true field 'over_powered' in player config for easy walkthrough.

    Notes: Game class work only at current machine - not enought resources(no fonts).
    Also ui not work correctly at other resolution.
    There also some problems with balance. (High difficult)
    
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game")

        cfg = get_cfg("game")
        self.THEME = cfg["theme"]
        self.SCREEN_SIZE = cfg["screen_size"]
        self.BACKGROUND_COLOR = cfg["background_color"]
        self.FRAMERATE = cfg["framerate"]
        self.FPS_SHOW = cfg["fps_show"]
        self.TUTORIAL_SHOW = cfg["tutorial_show"]

        img = get_image("explosion.gif")
        Explosion.images = [img, pygame.transform.flip(img, 1, 1)]

        if cfg["fullscreen"]:
            self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.ui_handler = UIHandler(get_cfg("ui"), self.screen)
        self.clock = pygame.time.Clock()
        self.groups = {
            "player": pygame.sprite.RenderUpdates(),
            "enemy": pygame.sprite.RenderUpdates(),
            "projectile": pygame.sprite.RenderUpdates(),
            "pickup": pygame.sprite.RenderUpdates(),
            "other": [],
        }
        if self.FPS_SHOW:
            self.fps_meter = FPSMeter(self.ui_handler)
        if self.TUTORIAL_SHOW:
            self.tutorial = Tutorial(get_cfg("tutorial"), self.screen, self.ui_handler, self)

        self.state = "prestarted"
        
    def start(self):
        """Initiate game objects and launch main cycle."""
        self.fill_groups()
        
        while True:
            self.time_delta = self.clock.tick(self.FRAMERATE)/1000
            self.update()
            self.draw()
            
    def fill_groups(self):
        self.player = Player(
            get_cfg("player"), self.ui_handler, self.SCREEN_SIZE,
            spawn_pos=(self.SCREEN_SIZE[0]/2, self.SCREEN_SIZE[1]/2)
        )
        specks = {
            "player": self.player.specks,
            "player_shooting": self.player.shooting
        }

        self.leveling = Leveling(self.screen, self.ui_handler, specks)

        heal_spawner = Spawner(
            cfg=get_cfg("spawners")["heal"], obj_cfg=get_cfg("heal"),
            obj_class=Heal, group=self.groups["pickup"],
            ui_handler=self.ui_handler, score=self.leveling, limits=self.SCREEN_SIZE
        )
        self.wave_manager = WaveManger(
            cfg=get_cfg("waves"),
            group=self.groups["enemy"], ui_handler=self.ui_handler,
            leveling=self.leveling, field_size=self.SCREEN_SIZE, player=self.player
        )

        self.groups["player"].add(self.player)
        self.groups["other"].extend([
            heal_spawner, self.wave_manager, self.leveling
        ])
            
    def update(self):
        self.update_events()
        self.update_groups()

        if self.FPS_SHOW:
            self.fps_meter.add(self.clock.get_fps())
            self.fps_meter.update()
        if self.TUTORIAL_SHOW and self.state == "prestarted":
            self.tutorial.update()

        self.ui_handler.update(self.time_delta)

        self.win_check()

    def update_events(self):
        """Handle events according to state."""
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if self.state == "prestarted":
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE or not self.TUTORIAL_SHOW:
                    if self.TUTORIAL_SHOW:
                        self.tutorial.close()
                    self.wave_manager.start()
                    self.state = "running"
                    self.start_time = time.time()
            elif self.state == "running":
                if e.type == WAVES_ENDED.type:
                    self.state = "win"
                if e.type == PLAYER_LOSE.type:
                    self.state = "lose"
            elif self.state == "end":
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.restart()
            
            self.ui_handler.process_events(e)
    
    def update_groups(self):
        """Trying to update groups, if fails update every element separately."""
        if self.state in ("prestarted", "lose", "paused", "end"):
            return

        for group in self.groups.values():
            try:
                group.update(groups=self.groups, time_delta=self.time_delta)
            except AttributeError:
                for updateable in group:
                    updateable.update(groups=self.groups, time_delta=self.time_delta)
    
    def draw(self):
        """Draw sprites groups, if fails draw every element separately, if fails pass."""
        self.screen.fill(self.BACKGROUND_COLOR)

        if self.state == "lose":
            return

        for group in list(self.groups.values())[:-1]:
            group.draw(self.screen)
        for service_obj in self.groups["other"]:
            try:
                service_obj.draw(self.screen)
            except AttributeError:
                pass
            
        self.ui_handler.draw()

        pygame.display.update()
    
    def win_check(self):
        """Create win-lose ui if neccesary."""
        if self.state not in ("win", "lose"):
            return
        
        if self.state == "win":
            self.win_label = self.ui_handler.add(
                "win_label", UILabel, ["center"],
                text="You win! Thanks for playing!", class_id="@state_label"
            )
            self.time_label = self.ui_handler.add(
                "time_label", UILabel, ["center"],
                text="Your time: {} s".format(round(time.time() - self.start_time, 2)),
                class_id="@state_label"
            )
        elif self.state == "lose":
            self.lose_label = self.ui_handler.add(
                "lose_label", UILabel, ["center"],
                text="You lose! (esc - restart)", class_id="@state_label"
            )

        self.state = "end"
    
    def restart(self):
        """Not Implemented
        # Use smth like SessionsManager and rename Game to Session?
        """
        self = Game()
        self.start()


if __name__ == "__main__":
    game = Game()
    game.start()
