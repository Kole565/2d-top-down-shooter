"""Provide Marker UI class."""
import pygame


class Marker(pygame.sprite.Sprite):

    def __init__(self, spawn_pos):
        super().__init__()

        self.radius = 10
        self.life = 2
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        color = [200, 0, 0]
        pygame.draw.circle(self.image, color, [self.radius, self.radius], self.radius)

        self.x, self.y = spawn_pos
        self.rect.x, self.rect.y = spawn_pos

        self.group = "ui"

    def update(self, *args, **kwargs):
        if not self.life:
            self.kill()

        self.life -= 1

    def on_collision(self, *args, **kwargs):
        pass
