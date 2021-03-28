import pygame,sys,math,os,random,time
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
    x = 0
    rects = []
    tiles_2 = []
    try:
        for tile in tiles[tiles_list[0]]:
            surf.blit(tile, (x, y))
            tiles_2.append(tile)
            rects.append(pygame.Rect(x, y, tile_size, tile_size))
            if y + tile_size >= surface.get_height():
                x += tile_size 
                y = 0
            else:
                y += 32
        print(y)
        return rects, tiles_2
    except IndexError:
        for ts in tiles:
            for tile in tiles[ts]:
                surf.blit(tile, (x, y))
                rects.append(pygame.Rect(x, y, tile_size, tile_size))
                tiles_2.append(tile)
                y += 32
            x += 32
        return rects, tiles_2

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
#------grid layout-------------------------------------------------------------------------------------------
def set_grid_layout(surf, grid_size_x, grid_size_y):
    grid_rects = []
    for i in range(SCREEN_SIZE[1]//grid_size_y):
        for j in range(SCREEN_SIZE[0]//grid_size_x):
            grid_rects.append(pygame.Rect(j*tile_size, i*tile_size, tile_size, tile_size))
    return grid_rects
grid_rects = set_grid_layout(surface, tile_size, tile_size)
#------get the tiles key dict--------------------------------------------------------------------------------
def make_dict(tiles_dict, rects):
    end_dict = {}
    for tiles in tiles_dict:
        for tile, rect in zip(tiles_dict[tiles], rects):
            end_dict[tile] = rect
    return end_dict
rects, tiles2 = render_spef_tiles(surface, current_tile_list)
tile_dict = make_dict(tiles, rects)
#------handling the current tile-----------------------------------------------------------------------------
global current_tile
current_tile = None
def change_tile(collision_obj, rects_list, tile_list):
    tile = 0
    global current_tile
    for rect, tile in zip(rects_list, tile_list):
        if collision_obj.colliderect(rect):
            current_tile = tile
    return current_tile
#------making the game map-----------------------------------------------------------------------------------
game_map = {}
def render_game_map(surf):
    for rect in game_map:
        data = rect
        surf.blit(game_map[rect], (int(data[0]), int(data[2])))
#------grid rect thing---------------------------------------------------------------------------------------
needed_grid_rect = pygame.Rect(16, 16, tile_size, tile_size)
grid_stuff = ""
#------main method-------------------------------------------------------------------------------------------
if __name__ == '__main__':
    while True:
        rects, tiles2 = render_spef_tiles(surface, current_tile_list)
        surface.fill((0,0,0))
        render_game_map(surface)
        tile_bar().render(surface)
        mx, my = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mx//2, my//2, 1, 1)
        for grid_rect in grid_rects:
            if grid_rect.colliderect(mouse_rect):
                try:
                    surface.blit(current_tile, (grid_rect.x, grid_rect.y))
                    needed_grid_rect = grid_rect
                except TypeError:
                    pass
        grid_stuff = needed_grid_rect.x, ';', needed_grid_rect.y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_collision_test(name_rects, mouse_rect)
                    change_tile(mouse_rect, rects, tiles2)
            if event.type == MOUSEWHEEL:
                game_map[grid_stuff] = current_tile
            if event.type == KEYDOWN:
                if event.key == 'K_z':
                    pass
        screen.blit(pygame.transform.scale(surface, SCREEN_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
