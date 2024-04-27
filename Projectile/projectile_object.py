import pygame
import math
import random


# Initialize Pygame
pygame.init()

# Screen dimensions and frame rate
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FRAME_RATE = 60

# Set up the display
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Metal Dug - Test - Projectile")

# Define constants for colors
RED = (255, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)

# Define constants for the game objects
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
PROJECTILE_RADIUS = 6
SPRITE_WIDTH = 30
SPRITE_HEIGHT = 30

class Collisions:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))

    def collide(self, other_object):
        """
        Check collision with another GameObject.
        """
        if (self.x < other_object.x + other_object.width and
            self.x + self.width > other_object.x and
            self.y < other_object.y + other_object.height and
            self.y + self.height > other_object.y):
            return True
        return False

class Sprite(Collisions):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.respawn()

    def respawn(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)

class Player(Collisions):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vel = 5

    def draw(self, win):
        super().draw(win)

class Projectile(Collisions):
    def __init__(self, x, y, radius, color, angle):
        super().__init__(x, y, radius * 2, radius * 2)
        self.radius = radius
        self.color = color
        self.angle = angle
        self.speed = 50

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x + self.radius), int(self.y + self.radius)), self.radius)

        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

def redraw_game_window(player, projectiles, cursor_pos, sprite):
    win.fill((0, 0, 0))
    player.draw(win)
    sprite.draw(win)
    for bullet in projectiles:
        bullet.draw(win)
    pygame.draw.circle(win, GREEN, cursor_pos, 5)  # Draw a green dot at cursor position
    pygame.display.update()

def get_angle(player_x, player_y, mouse_x, mouse_y):
    rel_x, rel_y = mouse_x - player_x, mouse_y - player_y
    return math.atan2(rel_y, rel_x)

# Main loop
player = Player(50, 50, PLAYER_WIDTH, PLAYER_HEIGHT)
projectiles = []
sprite = Sprite(500, 200, SPRITE_WIDTH, SPRITE_HEIGHT)

run = True
clock = pygame.time.Clock()
while run:
    clock.tick(FRAME_RATE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click to shoot
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = get_angle(player.x + player.width / 2, player.y + player.height / 2, mouse_x, mouse_y)
                projectiles.append(Projectile(player.x + player.width / 2, player.y + player.height / 2, PROJECTILE_RADIUS, CYAN, angle))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and player.x > player.vel:
        player.x -= player.vel
    elif keys[pygame.K_d] and player.x < SCREEN_WIDTH - player.width - player.vel:
        player.x += player.vel

    # Remove projectiles that go off-screen
    projectiles = [bullet for bullet in projectiles if 0 < bullet.x < SCREEN_WIDTH and 0 < bullet.y < SCREEN_HEIGHT]
    # Check for collisions between projectiles and the sprite
    for bullet in projectiles:
        if sprite.collide(bullet):
            sprite.respawn()
            projectiles.remove(bullet)

    cursor_pos = pygame.mouse.get_pos()
    redraw_game_window(player, projectiles, cursor_pos, sprite)

pygame.quit()