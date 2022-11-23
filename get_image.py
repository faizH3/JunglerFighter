import pygame

def getImage(lsName, sprite_img, range_a, range_b, name_img_json, scale):
	for x in range(range_a, range_b):
		f = sprite_img.parse_sprite(f'{name_img_json}{x}.png')
		img = pygame.transform.scale(f, (f.get_width()*scale, f.get_height()*scale))
		lsName.append(img)
