import pygame
from Config import WIDTH, HEIGHT
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_images()
        self.image = self.animations['idle_right'][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = 'right'

        self.speed = 8
        self.jump_force = -14
        self.y_vel = 0
        self.gravity = 0.5
        self.max_gravity = 15
        self.on_ground = False

        self.current_animation = 'idle_right'
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0

        self.world_shift_x = 0
        self.world_shift_y = 0

    def load_images(self):
        self.animations = { 
            'idle_right': [pygame.image.load(f'My Platformer/Player Graphics/idle_right/{i}.png') for i in range(5)],
            'idle_left': [pygame.image.load(f'My Platformer/Player Graphics/idle_left/{i}.png') for i in range(5)],
            'run_right': [pygame.image.load(f'My Platformer/Player Graphics/run_right/{i}.png') for i in range(6)],
            'run_left': [pygame.image.load(f'My Platformer/Player Graphics/run_left/{i}.png') for i in range(6)],
            'jump_right': [pygame.image.load(f'My Platformer/Player Graphics/jump_right/{i}.png') for i in range(1)],
            'jump_left': [pygame.image.load(f'My Platformer/Player Graphics/jump_left/{i}.png') for i in range(1)],
            'fall_right': [pygame.image.load(f'My Platformer/Player Graphics/fall_right/{i}.png') for i in range(1)],
            'fall_left': [pygame.image.load(f'My Platformer/Player Graphics/fall_left/{i}.png') for i in range(1)]
        }

    def update(self, keys, tile_rects):
        dx = 0
        dy = self.y_vel

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 25:
            dx = -self.speed
            self.direction = 'left'
            if self.on_ground:
                self.current_animation = 'run_left'
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x < (WIDTH - 25 - self.image.get_width()):
            dx = self.speed
            self.direction = 'right'
            if self.on_ground:
                self.current_animation = 'run_right'
        else:
            if self.on_ground:
                if self.direction == 'left':
                    self.current_animation = 'idle_left'
                else:
                    self.current_animation = 'idle_right'

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.y_vel = self.jump_force
            self.on_ground = False
            if self.direction == 'left':
                self.current_animation = 'jump_left'
            else:
                self.current_animation = 'jump_right'

        self.y_vel += self.gravity
        if self.y_vel > self.max_gravity:
            self.y_vel = self.max_gravity

        self.rect.x += dx
        self.check_collisions(tile_rects, dx, 0)
        self.rect.y += dy
        self.check_collisions(tile_rects, 0, dy)

        if dy > 0.5:
            self.on_ground = False

        # Respawn
        if self.rect.y > HEIGHT:
            self.rect.y = 370
            self.y_vel = 0
            self.dy = 0
            self.rect.x = 100
            self.dx = 0
            self.world_shift_x = 0
            self.world_shift_y = 0

        if not self.on_ground:
            if self.y_vel > 0:
                if self.direction == 'left':
                    self.current_animation = 'fall_left'
                else:
                    self.current_animation = 'fall_right'

        self.update_animation()

        # X world shift
        if self.rect.right > WIDTH - 400:  # Moving Right
            self.world_shift_x -= self.speed
            self.rect.right = WIDTH - 400

        elif self.rect.left < 400:  # Moving Left
            if self.world_shift_x < 0:
                self.world_shift_x += self.speed
                self.rect.left = 400

    def check_collisions(self, tile_rects, dx, dy):
        for tile in tile_rects:
            if self.rect.colliderect(tile):
                if dx > 0:  # Moving right
                    self.rect.right = tile.left
                elif dx < 0:  # Moving left
                    self.rect.left = tile.right
                if dy > 0:  # Falling down
                    self.rect.bottom = tile.top
                    self.y_vel = 0
                    self.on_ground = True
                elif dy < 0:  # Jumping up
                    self.rect.top = tile.bottom
                    self.y_vel = 0

    def update_animation(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            new_image = self.animations[self.current_animation][self.current_frame]
            new_rect = new_image.get_rect(midbottom=self.rect.midbottom)
            self.image = new_image
            self.rect = new_rect

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)