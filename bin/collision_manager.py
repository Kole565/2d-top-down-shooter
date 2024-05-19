import pygame


class CollisionManager:

    def __init__(self, groups):
        self.groups = groups

    def update(self, *args, **kwargs):
        for group_first in self.groups:
            groups_union = pygame.sprite.Group([sprites for sprites in self.groups[group_first]])
            collisions_dict = pygame.sprite.groupcollide(group_first, groups_union, False, False)

            if not collisions_dict:
                continue

            for subscriber, collisions in collisions_dict.items():
                if not collisions:
                    continue

                subscriber.on_collision(collisions)
