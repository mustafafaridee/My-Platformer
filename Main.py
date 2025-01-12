import pygame
import sys
from Tiles import *
from Player import Player
from Config import WIDTH, HEIGHT

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")

player = Player(100, 400)

def redraw():
    draw_tilemap(WIN, ldtk_data)
    player.draw(WIN)
    pygame.display.update()

clock = pygame.time.Clock()

def main():
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
        keys = pygame.key.get_pressed()
        player.update(keys, solid_tile_rects)
        redraw()

if __name__ == "__main__":
    main()