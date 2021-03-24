import pygame,sys,math,os,random
import data.scripts.block_handler as b_handler
import data.scripts.core_funcs as core_funcs
import data.scripts.text as Font
from pygame.locals import *
#------initialization------------------------------------------------------------------------------------
pygame.init()
clock = pygame.time.Clock()
SCREEN_SIZE = (992,592)
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
surface = pygame.Surface((SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
pygame.display.set_caption('!Pixle')
#-----block handler and Stuff----------------------------------------------------------------------------
Tile_size = 16
#------font rendering------------------------------------------------------------------------------------
font = Font.Font('data/images/fonts/small_font.png', (255,255,255))
#------spritesheet handler-------------------------------------------------------------------------------
def load_spritesheet(path):
    tiles = []
    for img in os.listdir(path):
        tiles.append(pygame.image.load(path+'/'+img))
    return tiles
tiles = load_spritesheet('data/images/tilesets/Gras_tiles')
#------tile bar-----------------------------------------------------------------------------------------
class tile_bar():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = surface.get_width() // 6
        self.height = surface.get_height()
    def render(self):
        pass
    def redner_tiles(self):
        pass
    def render_tile_names(self):
        pass

if __name__ == '__main__':
    while True:
        font.render('!Pixle', surface, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(pygame.transform.scale(surface, SCREEN_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(60)
