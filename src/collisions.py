import pygame

class Collisions:
    @staticmethod
    def check_collision(sprite,group):
        #checks collision between sprites
        collisions = pygame.sprite.spritecollide(sprite,group, False)
        return collisions
    @staticmethod
    def check_wall_collision(sprite, wall_group):
        #checks collision between sprite and walls.
        collisions = pygame.sprite.spritecollide(sprite, wall_group, False)
        for wall in collisions:
            if pygame.sprite.collide_rect(sprite, wall):
                if sprite.rect.bottom > wall.rect.top and sprite.rect.top < wall.rect.bottom:
                    if sprite.rect.right > wall.rect.left and sprite.rect.left < wall.rect.right:
                        # Collision will be handled.
                        sprite.handle_collision(wall)

    @staticmethod
    def check_projectile_collision(projectile, target_group):
        #checks collision between projectiles and targets
        collisions = pygame.sprite.spritecollide(projectile, target_group, False)
        for target in collisions:
            if pygame.sprite.collide_rect(projectile, target):
                # Collision are handled
                projectile.handle_collision(target)

class Projectile(pygame.sprite.Sprite):
    def handle_collision(self, collided_sprite):
        # method to handle collisions with another sprite (tiles or enemy)
        pass