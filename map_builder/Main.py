import pygame,sys,math,os,random,time,json
import data.scripts.text as Font
from json import JSONEncoder
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
    tile_imgs = {}
    for p in os.listdir(path):
        temp_tiles = []
        for img in os.listdir(path+'/'+p):
            temp_tiles.append([path+'/'+p+'/'+img,pygame.image.load(path+'/'+p+'/'+img)])
            tile_imgs[path+'/'+p+'/'+img] = pygame.image.load(path+'/'+p+'/'+img)
        tiles[p] = temp_tiles
    return tiles, tile_imgs
#------tiles and so on-----------------------------------------------------------------------------------
tiles, tile_imgs = load_spritesheet('data/images/tilesets')
tile_paths = {}
current_tile_list = []
def render_spef_tiles(surf, tiles_list):
    y = 50
    x = 0
    rects = []
    tiles_2 = []
    try:
        for tile in tiles[tiles_list[0]]:
            surf.blit(tile[1], (x, y))
            tiles_2.append(tile[1])
            rects.append(pygame.Rect(x, y, tile_size, tile_size))
            if y >= 200:
                x += tile_size * 2
                y = 50
            else:
                y += 32
        return rects, tiles_2
    except:
        for ts in tiles:
            for tile in tiles[ts]:
                surf.blit(tile[1], (x, y))
                rects.append(pygame.Rect(x, y, tile_size, tile_size))
                tiles_2.append(tile)
                if y >= 200:
                    x += tile_size  * 2
                    y = 50
                else:
                    y += 32
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
            end_tile = tile[1]
            end_dict[end_tile] = rect
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
            current_tile = tile[0]
    return current_tile
#------making the game map-----------------------------------------------------------------------------------
game_map = {}
def render_game_map(surf):
    for rect in game_map:
        data = rect
        surf.blit(pygame.image.load(game_map[rect]), (int(data[0]), int(data[1])))
#------grid rect thing---------------------------------------------------------------------------------------
needed_grid_rect = pygame.Rect(16, 16, tile_size, tile_size)
grid_stuff = ""
#------map saver---------------------------------------------------------------------------------------------
class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
def save_map(g_map, json_file="map.json"):
    with open(json_file, 'w') as f:
        end_dict = {}
        n = 0
        for item in game_map:
            tile_name = "tile"+str(n)
            tile_info = {}
            tile_info["rect"] = str(pygame.Rect(item[0], item[1], tile_size, tile_size))
            tile_info["image"] = str(game_map[item])
            end_dict[tile_name] = tile_info
            n += 1
        end_dict = json.dumps(end_dict)
        f.write(end_dict)
    f.close()
#------tile--------------------------------------------------------------------------------------------------
tile_count = 0
#------main method-------------------------------------------------------------------------------------------
if __name__ == '__main__':
    while True:
        rects, tiles2 = render_spef_tiles(surface, current_tile_list)
        surface.fill((0,0,0))
        render_game_map(surface)
        tile_bar().render(surface)
        mx, my = pygame.mouse.get_pos()
        font.render(str("x: "+str(mx)+" y: "+str(my)), surface, (tile_bar().width, 0))
        font.render("tiles: "+str(tile_count), surface, (tile_bar().width, 12))
        mouse_rect = pygame.Rect(mx//2, my//2, 1, 1)
        for grid_rect in grid_rects:
            if grid_rect.colliderect(mouse_rect):
                try:
                    surface.blit(pygame.image.load(current_tile), (grid_rect.x, grid_rect.y))
                    needed_grid_rect = grid_rect
                except:
                    pass
        grid_stuff = needed_grid_rect.x, needed_grid_rect.y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_map(game_map)
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_collision_test(name_rects, mouse_rect)
                    change_tile(mouse_rect, rects, tiles2)
                if event.button == 3:
                    game_map[grid_stuff] = current_tile
                    tile_count += 1
                if event.button == 4:
                    print("You scrolled up")
                if event.button == 5:
                    print("you scrolled down")
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    for grid_rect in grid_rects:
                        if grid_rect.colliderect(mouse_rect):
                            try:
                                del game_map[grid_stuff]
                                tile_count -= 1
                            except KeyError:
                                continue
            if event.type == MOUSEWHEEL:
                pass
        screen.blit(pygame.transform.scale(surface, SCREEN_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
