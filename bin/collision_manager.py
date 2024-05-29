import pygame


class CollisionManager:

    def __init__(self, groups):
        self.groups = groups

    def update(self, *args, **kwargs):
        for first_groups in self.groups:
            groups_union = pygame.sprite.Group(
                [sprites for sprites in self.groups[first_groups]]
            )
            collisions_dict = pygame.sprite.groupcollide(
                first_groups, groups_union, False, False
            )
            if not collisions_dict:
                continue

            for subscriber, collisions in collisions_dict.items():
                if not collisions:
                    continue

                subscriber.on_collision(collisions)
