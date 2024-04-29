import pygame

class PlayerHealth(pygame.sprite.Sprite):
    def __init__(self, screenHeight, startHealth=5):
        super().__init__()
        self.collision=False
        self.health = startHealth
        self.full_health_icon = pygame.image.load('assets/fullHealthIcon.png').convert_alpha()
        self.empty_health_icon = pygame.image.load('assets/emptyHealthIcon.png').convert_alpha()
        self.health_icons = []
        for _ in range(self.health):
            self.health_icons.append(self.full_health_icon)
        self.image = pygame.Surface(((self.full_health_icon.get_width()+5) * len(self.health_icons), self.full_health_icon.get_height()))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (30, screenHeight - 30)
        self.update_health_icons()

    def update_health_icons(self):
        self.image.fill((0, 0, 0))  # Clear the surface with transparent color
        for i, icon in enumerate(self.health_icons):
            self.image.blit(icon, (i * (self.full_health_icon.get_width() + 5), 0))
        self.image.set_colorkey((0, 0, 0))  # Set transparent colorkey

    def update_health(self, new_health):
        if new_health < 0:
            new_health = 0
        elif new_health > len(self.health_icons):
            new_health = len(self.health_icons)
        self.health = new_health
        self.health_icons = [self.full_health_icon] * self.health + [self.empty_health_icon] * (len(self.health_icons) - self.health)
        self.update_health_icons()

        if self.health == 0:
            self.gameOver()

    def gameOver(self):
        pass