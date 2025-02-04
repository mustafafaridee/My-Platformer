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
    1: pygame.transform.scale(get_tile(15, 1), (TILE_SIZE, TILE_SIZE)),  # Solid
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

BG_tile_rects = []
solid_tile_rects = []

def draw_tilemap(screen, ldtk_data):
    global BG_tile_rects, solid_tile_rects
    BG_tile_rects.clear()
    solid_tile_rects.clear()

    for layer in ldtk_data['levels'][0]['layerInstances']:
        if layer['__type'] == 'IntGrid' and layer['__identifier'] == 'IntGrid_layer':
            for i, tile_id in enumerate(layer['intGridCsv']):
                x = (i % layer['__cWid']) * TILE_SIZE
                y = (i // layer['__cWid']) * TILE_SIZE
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
                dest_x = tile['px'][0] * TILE_SIZE // 8
                dest_y = tile['px'][1] * TILE_SIZE // 8

                tile_image = get_tile(src_x // 8, src_y // 8)
                tile_image = pygame.transform.scale(tile_image, (TILE_SIZE, TILE_SIZE))
                screen.blit(tile_image, (dest_x, dest_y))