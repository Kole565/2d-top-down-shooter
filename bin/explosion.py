import pygame


class Explosion(pygame.sprite.Sprite):

    defautl_life = 12
    anim_len = 3
    images = []

    def __init__(self, actor):
        super().__init__()

        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)

        self.life = self.defautl_life

    def update(self, *args, **kwargs):
        self.life -= 1
        self.image = self.images[self.life // self.anim_len % 2]
        if self.life <= 0:
            self.kill()
