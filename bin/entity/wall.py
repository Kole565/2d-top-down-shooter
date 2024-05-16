import pygame


class Wall(pygame.sprite.Sprite):

    def __init__(self, cfg, spawn_pos=[0, 0]):
        super().__init__()

        self.image = pygame.Surface([cfg["size"], cfg["size"]])
        self.image.fill([0, 0, 0])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        pygame.draw.rect(self.image, cfg["color"], [0, 0, cfg["size"], cfg["size"]])

        self.side = "neutral"

        self.x, self.y = spawn_pos
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, *args, **kwargs):
        pass
