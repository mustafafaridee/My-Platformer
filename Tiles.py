import pygame
import json5
pygame.init()

TILE_SIZE = 40
def load_ldtk_file(file_path):
    with open(file_path, 'r') as file:
        data = json5.load(file)
        return data
    
ldtk_data = load_ldtk_file('My Platformer/Level_Map.ldtk')
sprite_sheet = pygame.image.load('My Platformer/TileMap.png')

def get_tile(x, y, width=8, height=8):
    tile = pygame.Surface((width, height), pygame.SRCALPHA)
    tile.blit(sprite_sheet, (0, 0), (x * width, y * height, width, height))
    return tile

tiles = {
    0: pygame.transform.scale(get_tile(0, 0), (TILE_SIZE, TILE_SIZE)),  # BG
    1: pygame.transform.scale(get_tile(15, 1), (TILE_SIZE, TILE_SIZE)),  # Solid
}

BG_tile_rects = []
solid_tile_rects = []

def draw_tilemap(screen, ldtk_data, world_shift_x, world_shift_y):
    global BG_tile_rects, solid_tile_rects
    BG_tile_rects.clear()
    solid_tile_rects.clear()

    for layer in ldtk_data['levels'][0]['layerInstances']:
        if layer['__type'] == 'IntGrid' and layer['__identifier'] == 'IntGrid_layer':
            for i, tile_id in enumerate(layer['intGridCsv']):
                x = (i % layer['__cWid']) * TILE_SIZE + world_shift_x
                y = (i // layer['__cWid']) * TILE_SIZE + world_shift_y
                if tile_id == 1:  # Solid
                    tile_image = tiles[1]
                    solid_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    solid_tile_rects.append(solid_rect)
                elif tile_id == 0:  # BG
                    tile_image = tiles[0]
                    screen.blit(tile_image, (x, y))
                    BG_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    BG_tile_rects.append(BG_rect)

    # Draw autolayer tiles
    for layer in ldtk_data['levels'][0]['layerInstances']:
        if 'autoLayerTiles' in layer:
            for tile in layer['autoLayerTiles']:
                src_x = tile['src'][0]
                src_y = tile['src'][1]
                dest_x = tile['px'][0] * TILE_SIZE // 8 + world_shift_x
                dest_y = tile['px'][1] * TILE_SIZE // 8 + world_shift_y

                tile_image = get_tile(src_x // 8, src_y // 8)
                tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))

                # Check for flipping rules
                if 'f' in tile and tile['f'] == 1:  # Flip horizontally
                    tile_image = pygame.transform.flip(tile_image, True, False)
                if 'f' in tile and tile['f'] == 2:  # Flip vertically
                    tile_image = pygame.transform.flip(tile_image, False, True)
                if 'f' in tile and tile['f'] == 3:  # Flip both horizontally and vertically
                    tile_image = pygame.transform.flip(tile_image, True, True)

                screen.blit(tile_image, (dest_x, dest_y))