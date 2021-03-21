import pygame,sys,math,os,random
import data.scripts.fonts as Fonts
import data.scripts.block_handler as b_handler
import data.scripts.core_funcs as core_funcs
import data.scripts.tile_bar as tile_bar
from pygame.locals import *
# some variables and stuff
pygame.init()
SCREEN_SIZE = (992,592)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
title = pygame.display.set_caption('!Pixle')
block_handler = b_handler.block_handler(16)
block_handler.set_grid_layout(screen, SCREEN_SIZE)
block_handler.open_tileset('data/images/tilesets/Gras_tiles/')
final_blocks = []
block_index = 0
current_rect = pygame.Rect(0, 0, 0, 0)
# text input
base_font = pygame.font.Font(None,32)
user_text = '0'
input_rect = pygame.Rect(0, 0, 200, 80)
rect_color = (255,255,255)
pygame.mouse.set_visible(False)
appending = False
while True:
	if int(user_text) < len(block_handler.blocks):
		block_index = int(user_text)
	else:
		user_text = '0'
	screen.fill((0, 0, 0))
	for block in final_blocks:
		screen.blit(block_handler.blocks[block_index], (block.x, block.y))
	appended_rect = pygame.Rect(block_handler.cb[0], block_handler.cb[1], block_handler.block_size, block_handler.block_size)
	cursor_pos = pygame.mouse.get_pos()
	if appending == True:
		if appended_rect not in final_blocks:
			final_blocks.append(appended_rect)

	# for i in range(9):
	# 	screen.blit(block_handler.blocks[i], (random.randint(0,62)*block_handler.block_size,random.randint(0,62)*block_handler.block_size))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_DOWN:
				appending = True
			if event.key == K_BACKSPACE:
			    user_text = user_text[:-1]	
			else:
				user_text += event.unicode
		if event.type == KEYUP:
			if event.key == K_DOWN:
				appending = False
	block_handler.cursor_collisions(screen, cursor_pos, block_handler.blocks[block_index])
	#input rendering
	pygame.draw.rect(screen,rect_color,input_rect,1)
	text_surface = base_font.render(user_text,True,(255,255,255))
	screen.blit(text_surface,input_rect)
	print(user_text)
	pygame.display.update()
	clock.tick(60)
