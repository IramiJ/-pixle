import pygame,sys,math,os,random
import data.scripts.block_handler as b_handler
import data.scripts.core_funcs as core_funcs
import data.scripts.text as Font
from pygame.locals import *
#------initialization------------------------------------------------------------------------------------
pygame.init()
clock = pygame.time.Clock()
SCREEN_SIZE = [992,592]
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
surface = pygame.Surface((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
pygame.display.set_caption('!Pixle')
#-----block handler and Stuff----------------------------------------------------------------------------
tile_size = 16
tile_scale = 1
true_scroll = [0, 0]
#------font rendering------------------------------------------------------------------------------------
font = Font.Font('data/images/fonts/small_font.png', (255,255,255))
#------spritesheet handler-------------------------------------------------------------------------------
def load_spritesheet(path):
    tiles = {}
    for p in os.listdir(path):
        temp_tiles = []
        for img in os.listdir(path+'/'+p):
            temp_tiles.append(pygame.image.load(path+'/'+p+'/'+img))
        tiles[p] = temp_tiles
        return tiles
tiles = load_spritesheet('data/images/tilesets')
#------tile bar-----------------------------------------------------------------------------------------
class tile_bar():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = surface.get_width() // 6
        self.height = surface.get_height()
        pygame.draw.line(surface, (255, 255, 255), (0, 56), (self.width, 56))
    def render(self,surf):
        render_tiles(surf, tiles)
        render_tile_names(surf, tiles)
def render_tiles(surf, tile_list):
    y = 32 + 50
    for tiles in tile_list:
        for tile in tile_list[tiles]:
            surf.blit(pygame.transform.scale(tile, (tile_size // tile_scale, tile_size // tile_scale)), [0, y])
            y += 24
    return y
def render_tile_names(surf, tile_list):
    y = 0
    for tile_name in tile_list:
        font.render(tile_name, surf, [0, y])
        y += 16
    return y

if __name__ == '__main__':
    while True:
        surface.fill((0,0,0))
        tile_bar().render(surface)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(pygame.transform.scale(surface, SCREEN_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
