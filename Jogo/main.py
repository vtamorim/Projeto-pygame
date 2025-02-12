import pygame
import time
import random
import os
from config import mostrar_opcoes
import pygame.freetype


            

pygame.init()
pygame.font.init()
font_path_title = pygame.freetype.Font('PixelifySans-VariableFont_wght.ttf',50)

font_path_options = pygame.freetype.Font('PixelifySans-VariableFont_wght.ttf',25)

dificuldade = ["Fácil","Médio","Díficil"]
width = 1000
height = 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

pygame.display.set_caption('Lâmina Fúngica')
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if first_option_rect.collidepoint(mouse):
                    print(1)
                elif second_option_rect.collidepoint(mouse):
                    mostrar_opcoes()
                elif three_option_rect.collidepoint(mouse):
                    running = False
                
    mouse = pygame.mouse.get_pos()


    screen.fill((255,255,255))
    title_surface, titlerect= font_path_title.render("Lâmina Fúngica", (0,0,0))
    titlerect = title_surface.get_rect(center = (width//2, height*0.12))
    screen.blit(title_surface,titlerect)

    first_option, first_option_rect = font_path_options.render("Jogar", (0,0,0))
    first_option_rect = first_option.get_rect(center = (width//2, height*0.40))
    screen.blit(first_option,first_option_rect)

    second_option, second_option_rect = font_path_options.render("Configurações", (0,0,0))
    second_option_rect = second_option.get_rect(center = (width//2, height* 0.54))
    screen.blit(second_option, second_option_rect)

    three_option, three_option_rect = font_path_options.render("Sair", (0,0,0))
    three_option_rect = three_option.get_rect(center = (width//2 , height * 0.68))
    screen.blit(three_option,three_option_rect)
    
    pygame.display.flip()

    clock.tick(60)  
pygame.quit()