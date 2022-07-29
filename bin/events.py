import pygame


powerup_button_click = {
    "powerup_1": pygame.event.Event(pygame.USEREVENT + 2),
    "powerup_2": pygame.event.Event(pygame.USEREVENT + 3),
    "powerup_3": pygame.event.Event(pygame.USEREVENT + 4),
    "powerup_4": pygame.event.Event(pygame.USEREVENT + 5),
    "powerup_5": pygame.event.Event(pygame.USEREVENT + 6),
    "powerup_6": pygame.event.Event(pygame.USEREVENT + 7),
}

WAVES_ENDED = pygame.event.Event(pygame.USEREVENT + 10)
PLAYER_LOSE = pygame.event.Event(pygame.USEREVENT + 11)
