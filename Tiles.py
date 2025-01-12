import pygame
import json5

pygame.init()

TILE_SIZE = 40

def load_ldtk_file(file_path):
    with open(file_path, 'r') as file:
        data = json5.load(file)
        return data

ldtk_data = load_ldtk_file('My Platformer/Test_Map.ldtk')

sprite_sheet = pygame.image.load('My Platformer/TileMap.png')

def get_tile(x, y, width=8, height=8):
    tile = pygame.Surface((width, height), pygame.SRCALPHA)
    tile.blit(sprite_sheet, (0, 0), (x * width, y * height, width, height))
    return tile

tiles = {
    0: pygame.transform.scale(get_tile(0, 0), (TILE_SIZE, TILE_SIZE)),  # BG
    1: pygame.transform.scale(get_tile(18, 18), (TILE_SIZE, TILE_SIZE))   # Grass top dirt
}

solid_tile_rects = []
bg_tile_rects = []

def draw_tilemap(screen, ldtk_data):
    global solid_tile_rects, bg_tile_rects
    solid_tile_rects.clear()
    bg_tile_rects.clear()

    # Draw background tiles first
    for layer in ldtk_data['levels'][0]['layerInstances']:
        if layer['__type'] == 'IntGrid' and layer['__identifier'] == 'IntGrid_layer':
            for i, tile_id in enumerate(layer['intGridCsv']):
                x = (i % layer['__cWid']) * TILE_SIZE
                y = (i // layer['__cWid']) * TILE_SIZE

                if tile_id == 1:  # Solid
                    tile_image = tiles[1]
                    screen.blit(tile_image, (x, y))
                    solid_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    solid_tile_rects.append(solid_rect)

                elif tile_id == 0:  # BG
                    tile_image = tiles[0]
                    screen.blit(tile_image, (x, y))
                    bg_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    bg_tile_rects.append(bg_rect)