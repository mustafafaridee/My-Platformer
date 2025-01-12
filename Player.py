import pygame
from Config import WIDTH, HEIGHT
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill((255, 255, 0))  # Yellow color for the player
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = 8
        self.jump_force = -12.5
        self.y_vel = 0
        self.gravity = 0.5
        self.max_gravity = 15
        self.on_ground = False

    def update(self, keys, tile_rects):
        dx = 0
        dy = self.y_vel

        if keys[pygame.K_LEFT] and self.rect.x > 25 or keys[pygame.K_a] and self.rect.x > 25:
            dx = -self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < (WIDTH-25-self.image.get_width()) or keys[pygame.K_d] and self.rect.x < (WIDTH-25-self.image.get_width()):
            dx = self.speed

        # Apply gravity
        if not self.on_ground:
            self.y_vel += self.gravity
            if self.y_vel > self.max_gravity:
                self.y_vel = self.max_gravity

        if self.rect.y > HEIGHT:
            self.rect.topleft = (100, 400)
            self.y_vel = 0

        # Check for collisions
        self.rect.x += dx
        self.on_ground = False
        for tile in tile_rects:
            if self.rect.colliderect(tile):
                if dx > 0:  # Moving right
                    self.rect.right = tile.left
                if dx < 0:  # Moving left
                    self.rect.left = tile.right

        self.rect.y += dy
        for tile in tile_rects:
            if self.rect.colliderect(tile):
                if dy > 0:  # Falling down
                    self.rect.bottom = tile.top
                    self.y_vel = 0
                    self.on_ground = True
                if dy < 0:  # Jumping up
                    self.rect.top = tile.bottom
                    self.y_vel = 0

        # Jumping
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.y_vel = self.jump_force

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)