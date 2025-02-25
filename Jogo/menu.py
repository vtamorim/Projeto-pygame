import pygame
import pygame.freetype
import csv
import os
import random
import json



pygame.init()
pygame.mixer.init()
pygame.freetype.init() 
slider_value_fps = 60
slider_handle_volume = 50
dif_sel = "Médio"
#pygame.mixer.music.set_volume(slider_handle_volume / 100)
width, height = 1000, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

font_path_title = pygame.freetype.Font('Jogo/PixelifySans-VariableFont_wght.ttf', 50)
font_path_options = pygame.freetype.Font('Jogo/PixelifySans-VariableFont_wght.ttf', 25)
banner=  pygame.image.load('pixil-frame-0 (11).png')
banner=  pygame.transform.scale(banner,(1000,720))
menu_fx = pygame.mixer.Sound('audio/menugame.mp3')
slider_handle_volume = 1
menu_fx.play()
def menu(screen, font_path_title, font_path_options, clock, slider_value_fps, slider_handle_volume, dif_sel="Médio"):
    import game
    running = True

    while running:
        if slider_handle_volume == 0:
            volume= 0
        else:
            volume = 5 / 100
        menu_fx.set_volume(volume)
        screen.blit(banner,(0,0))
        mouse = pygame.mouse.get_pos()

        title_surface, titlerect = font_path_title.render("Frozen Wasteland", (255, 255, 255))
        titlerect = title_surface.get_rect(center=(500, 100))
        screen.blit(title_surface, titlerect)

        # Botões
        first_option, first_option_rect = font_path_options.render("Iniciar", ((255,255,255)))
        first_option_rect = first_option.get_rect(center=(500, 300))
        pygame.draw.rect(screen, (255, 255, 255),( first_option_rect.x - 32, first_option_rect.y - 15, first_option_rect.width + 65, first_option_rect.height + 30))
        pygame.draw.rect(screen, (9, 13, 71), ( first_option_rect.x - 20, first_option_rect.y - 10, first_option_rect.width + 40, first_option_rect.height + 20))
        screen.blit(first_option, first_option_rect)

        second_option, second_option_rect = font_path_options.render("Configurações", ((255,255,255)))
        second_option_rect = second_option.get_rect(center=(500, 400))
        pygame.draw.rect(screen, (255, 255, 255),( second_option_rect.x - 32, second_option_rect.y - 15 , second_option_rect.width + 65, second_option_rect.height + 30))
        pygame.draw.rect(screen, (1, 49, 60),( second_option_rect.x - 20, second_option_rect.y - 10, second_option_rect.width + 40, second_option_rect.height + 20))
        screen.blit(second_option, second_option_rect)

        three_option, three_option_rect = font_path_options.render("Sair", ((255,255,255)))
        three_option_rect = three_option.get_rect(center=(500, 500))
        pygame.draw.rect(screen, (255, 255, 255),( three_option_rect.x - 32, three_option_rect.y - 15, three_option_rect.width + 65, three_option_rect.height + 30))
        pygame.draw.rect(screen, (71,17 ,107 ), ( three_option_rect.x - 20, three_option_rect.y - 10, three_option_rect.width + 40, three_option_rect.height + 20))
        screen.blit(three_option, three_option_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if first_option_rect.collidepoint(mouse):
                        menu_fx.stop()
                        game.wow(slider_value_fps,slider_handle_volume,dif_sel,volume)
                    elif second_option_rect.collidepoint(mouse):
                        config(screen, font_path_title, font_path_options, clock)  # Chama config()
                    elif three_option_rect.collidepoint(mouse):
                        running = False  

        clock.tick(60)

def config(screen, font_path_title, font_path_options, clock):


    def mostrar_opcoes():
        pygame.display.set_caption("Opções")
    dificuldade = ['Fácil', 'Médio', 'Difícil']
    dif_sel = "Médio"
    largura_borda = 1
    padding = 30        
    dif_padding = 600
    mostrar_opcoes = False
    setinha = pygame.transform.scale(pygame.image.load('Jogo/setinha.png'), (30, 30))
    min_value = 0
    max_value_fps = 120
    max_value_volume = 100
    slider_value_fps = (max_value_fps - min_value) * 0.5
    slider_rect_fps = pygame.Rect(300, 720//2, 400, 10)
    slider_handle_fps = pygame.Rect(380, 720//2 - 5, 20, 20)
    
    slider_rect_volume = pygame.Rect(300, 430, 400, 10)
    slider_handle_volume = pygame.Rect(380, 430 - 5, 20, 20)
    slider_value_volume = (max_value_fps - min_value) * 0.5

    def draw_slider_fps():
        pygame.draw.rect(screen, (220, 220, 220), slider_rect_fps)
        pygame.draw.rect(screen,  (0,93,162), slider_handle_fps)

    def update_slider_fps(x_position):
        nonlocal slider_handle_fps, slider_value_fps  
        if slider_rect_fps.left < x_position < slider_rect_fps.right:
            slider_handle_fps.centerx = x_position
            slider_value_fps = min_value + ((slider_handle_fps.centerx - slider_rect_fps.left) / slider_rect_fps.width) * (max_value_fps - min_value)
    
    def draw_slider_volume():
        pygame.draw.rect(screen, (220, 220, 220), slider_rect_volume)
        pygame.draw.rect(screen, (0,93,162), slider_handle_volume)

    def update_slider_volume(x_position):
        nonlocal slider_handle_volume, slider_value_volume  
        if slider_rect_volume.left < x_position < slider_rect_volume.right:
            slider_handle_volume.centerx = x_position
            slider_value_volume = min_value + ((slider_handle_volume.centerx - slider_rect_volume.left) / slider_rect_volume.width) * (max_value_volume - min_value)

    running = True
    dragging_fps = False
    dragging_volume = False

    while running:
        screen.blit(banner,(0,0))
        pygame.draw.rect(screen, (255, 255, 255),( 130, 260,700,60))
        pygame.draw.rect(screen, (71,17 ,107 ), ( 145, 265, 670, 50))
        mouse = pygame.mouse.get_pos()
        arrow = pygame.transform.scale(pygame.image.load("Jogo/arrow.png"),(30,30))
        arrow_rect = arrow.get_rect(topleft = (0,0))
        pygame.draw.rect(screen, (255, 255, 255),( 130, 330,700,60))
        pygame.draw.rect(screen, (71,17 ,107 ), ( 145, 335, 670, 50))
        pygame.draw.rect(screen, (255, 255, 255),( 130, 400,700,60))
        pygame.draw.rect(screen, (71,17 ,107 ), ( 145, 405, 670, 50))
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 350 < mouse[0] < 620 and 260 < mouse[1] < 310:
                        mostrar_opcoes = not mostrar_opcoes

                if slider_handle_fps.collidepoint(event.pos):
                    dragging_fps = True
                if slider_handle_volume.collidepoint(event.pos):
                    dragging_volume = True
                if arrow_rect.collidepoint(mouse):
                    menu(screen, font_path_title, font_path_options, clock, slider_value_fps,slider_handle_volume,dif_sel)
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_fps = False
                dragging_volume = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging_fps:
                    update_slider_fps(event.pos[0])
                if dragging_volume:
                    update_slider_volume(event.pos[0])

        draw_slider_fps()
        draw_slider_volume()

        text_surface, _ = font_path_options.render(f"{slider_value_fps:.0f}",(255,255,255))
        screen.blit(text_surface, (740, 355))
        fps_config, fps_rect = font_path_options.render("FPS:", (255, 255, 255))
        fps_rect = fps_config.get_rect(midleft = (width//6, height*0.5))
        screen.blit(fps_config,fps_rect)


        text_volum,_ = font_path_options.render(f"{slider_value_volume:.0f}",(255,255,255))
        screen.blit(text_volum, (740, 425))
        vol_config, vol_rect = font_path_options.render("Volume:", (255, 255, 255))
        vol_rect = vol_config.get_rect(midleft = (width//6, height*0.6))
        screen.blit(vol_config, vol_rect)

        if mostrar_opcoes:
            for niveis in dificuldade:
                yzin = 15
                texto, texto_rect = font_path_options.render(niveis, (255, 255, 255))
                texto_rect = texto.get_rect(center=(width // 2.2, dif_padding + 135))
                pygame.draw.rect(screen, (255, 255, 255), (321, texto_rect.y - yzin, 282, 47), largura_borda)
                pygame.draw.rect(screen, (71,17,107),(322,texto_rect.y-14,280,45))
                screen.blit(texto, texto_rect) 
                dif_padding += 46
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if texto_rect.collidepoint(mouse):
                            mostrar_opcoes = False
                            dif_sel = str(niveis)
    
        pygame.draw.line(screen, (71,17,107), (321, 312), (601, 312), 5)
        setinha_rect = setinha.get_rect(topleft = (width//2 + 70,height*0.38))
        title_config, config_rect = font_path_title.render("Configurações", (255,255,255))
        config_rect = title_config.get_rect(center = (width//2, height*0.12))

        dif_config, dif_rect = font_path_options.render("Dificuldade", (255,255,255))
        dif_rect = dif_config.get_rect(midleft = (width//6, height*0.4))

        screen.blit(title_config, config_rect)
        screen.blit(dif_config, dif_rect)
        select_dif, sel_rect = font_path_options.render(dif_sel, (255, 255, 255))
        sel_rect = select_dif.get_rect(center = (width//2.2, height*0.4))

        screen.blit(select_dif, sel_rect)
        screen.blit(setinha, setinha_rect)
        dif_padding = 200
        
        screen.blit(arrow,arrow_rect)
        
       
        pygame.display.flip()
        clock.tick(60)

    mostrar_opcoes()



menu(screen, font_path_title, font_path_options, clock,slider_value_fps,slider_handle_volume,dif_sel)