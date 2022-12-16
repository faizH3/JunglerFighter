import pygame

def bground(surface):
    bg_img = []
    for x in range(0, 12):
        img = pygame.image.load(f'assets/images/background/{x}.png').convert_alpha()
        bg_img.append(img)
    
    for i in  bg_img:
        surface.blit(i, (0, -150))
