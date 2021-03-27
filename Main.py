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
#------tiles and so on-----------------------------------------------------------------------------------
tiles = load_spritesheet('data/images/tilesets')
current_tile_list = []
def render_spef_tiles(surf, tiles_list):
    y = 50
    try:
        for tile in tiles[tiles_list[0]]:
            surf.blit(tile, (0, y))
            y += 32
    except IndexError:
        for ts in tiles:
            for tile in tiles[ts]:
                surf.blit(tile, (0, y))
                y += 32
            return 0;

#------tile bar-----------------------------------------------------------------------------------------
class tile_bar():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = surface.get_width() // 6
        self.height = surface.get_height()
        self.surf = pygame.Surface((self.width, self.height))
    def render(self,surf):
        self.surf.fill((48, 97, 32))
        surf.blit(self.surf, (0, 0))
        render_spef_tiles(surf, current_tile_list)
        render_tile_names(surf, tiles)
        pygame.draw.line(surface, (255, 255, 255), (0, 48), (self.width, 48))
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
def calc_name_rects(tile_names):
    name_rects = {}
    y = 0
    for tile_name in tile_names:
        name_rects[tile_name] = pygame.Rect(0, y, font.width(tile_name),8)
        y += 16
    return name_rects
def mouse_collision_test(name_rects, mouse_rect):
    for rect in name_rects:
        if name_rects[rect].colliderect(mouse_rect):
            current_tile_list.clear()
            current_tile_list.append(rect)
name_rects = calc_name_rects(tiles)
if __name__ == '__main__':
    while True:
        screen.fill((0,0,0))
        tile_bar().render(surface)
        mx, my = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mx//2, my//2, 1, 1)
        pygame.draw.rect(screen, (255,0,0), mouse_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_collision_test(name_rects, mouse_rect)
        screen.blit(pygame.transform.scale(surface, SCREEN_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
