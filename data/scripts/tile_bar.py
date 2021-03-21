import pygame
from pygame.locals import *

pygame.init()

class tile_bar():
	def __init__(self,x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
	def render_tile_text(self, x_pos, y_pos, font_path, tile_text, surf):
	    text_font = Fonts.Font(font_path)
	    text_font.render(surf, tile_text, (x_pos, y_pos))
