import pygame
import math
from pygame.locals import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x,y, radius, angle, color):
        super().__init__(x,y,radius * 2, radius * 2)
        self.radius = radius
        #self.image = pygame.Surface((5,5))
        #self.image.fill((0,0,0))
        self.rect = self.image.get_rect(center=(x,y))
        self.angle = angle
        self.speed = 50 
        self.color = (0,0,0)

    def update(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x + self.radius), int(self.y + self.radius)), self.radius)

        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed

        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

    def handle_collision(self, collided_sprite):
        self.kill()

    def redraw_game_window(tank, projectiles, cursor_pos, sprite):
            screen.fill((0, 0, 0))
            tank.draw(screen)
            sprite.draw(screen)
            for bullet in projectiles:
                bullet.draw(screen)
            pygame.draw.circle(screen, (0,255,0), cursor_pos, 5)  # Draw a green dot at cursor position
            pygame.display.update()

    def get_angle(player_x, player_y, mouse_x, mouse_y):
        rel_x, rel_y = mouse_x - player_x, mouse_y - player_y
        return math.atan2(rel_y, rel_x)