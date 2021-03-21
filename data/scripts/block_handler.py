import pygame, random, os

pygame.init()

class block_handler():
    def __init__(self, block_size):
        self.block_size = block_size
        self.cb = [0, 0] # determines the current block position
        self.rects = []
        self.blocks = []
    def set_grid_layout(self, surface, screen_size):
        for y in range(screen_size[1] // self.block_size):
            for x in range(screen_size[0] // self.block_size):
                self.rects.append(pygame.Rect(x*(self.block_size), y*(self.block_size), self.block_size, self.block_size))
        return self.rects

    def open_tileset(self, path):
        block_ids = os.listdir(path)
        for block in block_ids:
            self.blocks.append(pygame.image.load(path+block))
        return self.blocks

    def cursor_collisions(self, surf, cursor_pos, selected_tile):
        cursor_rect = pygame.Rect(cursor_pos[0], cursor_pos[1], 1, 1)
        for rect in self.rects:
            if rect.colliderect(cursor_rect):
                surf.blit(selected_tile, (rect.x, rect.y))
                self.cb[0] = rect.x
                self.cb[1] = rect.y
        return cursor_rect