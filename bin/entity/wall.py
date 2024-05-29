"""Provide implementation of Wall obstacle class."""
import pygame


class Wall(pygame.sprite.Sprite):
    """Create solid block for blocking way."""

    def __init__(self, cfg, spawn_pos=[0, 0]):
        """Init obstacle config and position."""
        super().__init__()

        self.image = pygame.Surface([cfg["size"], cfg["size"]])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, cfg["color"], self.rect)

        self.group = "obstacle"
        self.rect.x, self.rect.y = spawn_pos
        self.size = cfg["size"]
