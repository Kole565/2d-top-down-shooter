import pygame

from pygame_gui.elements import UITextBox


class Tutorial:

    """Frame with several labels, screen fade effect."""

    def __init__(self, cfg, screen, ui_handler, controller):
        self.fade_intensity = cfg["fade_intensity"]
        self.tutorial = cfg["tutorial"]

        self.screen = screen
        self.ui_handler = ui_handler
        self.controller = controller

        self.init_labels()

    def init_labels(self):
        self.labels = pygame.sprite.Group()
        for name in self.tutorial:
            self.labels.add(self.ui_handler.add_absolute(
                name, UITextBox,
                self.tutorial[name]["relative_position"], self.tutorial[name]["relative_size"],
                html_text=self.tutorial[name]["text"], class_id="@tutorial_box"
            ))

    def update(self):
        image = pygame.Surface(self.screen.get_size())
        image.set_alpha(self.fade_intensity)
        self.screen.blit(image, (0, 0))

        self.labels.draw(self.screen)

    def close(self):
        self.controller.paused = False
        self.ui_handler.remove(*list(self.tutorial.keys()))
        self.labels.empty()
