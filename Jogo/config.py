import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 720))
clock = pygame.time.Clock()

def mostrar_opcoes():
    pygame.display.set_caption("Opções")
    dificuldade = ['Fácil', 'Médio', 'Difícil']
    dif_sel = "Selecionar"
    largura_borda = 1
    padding = 30        
    dif_padding = 600
    mostrar_opcoes = False
    setinha = pygame.transform.scale(pygame.image.load('setinha.png'), (30, 30))
    min_value = 0
    max_value_fps = 120
    max_value_volume = 100
    slider_value_fps = (max_value_fps - min_value) * 0.5
    slider_rect_fps = pygame.Rect(300, 720//2, 400, 10)
    slider_handle_fps = pygame.Rect(380, 720//2 - 5, 20, 20)
    
    slider_rect_volume = pygame.Rect(300, 500, 400, 10)
    slider_handle_volume = pygame.Rect(380, 500 - 5, 20, 20)
    slider_value_volume = (max_value_fps - min_value) * 0.5

    def draw_slider_fps():
        pygame.draw.rect(screen, (220, 220, 220), slider_rect_fps)
        pygame.draw.rect(screen, (0, 0, 0), slider_handle_fps)

    def update_slider_fps(x_position):
        nonlocal slider_handle_fps, slider_value_fps  
        if slider_rect_fps.left < x_position < slider_rect_fps.right:
            slider_handle_fps.centerx = x_position
            slider_value_fps = min_value + ((slider_handle_fps.centerx - slider_rect_fps.left) / slider_rect_fps.width) * (max_value_fps - min_value)
    
    def draw_slider_volume():
        pygame.draw.rect(screen, (220, 220, 220), slider_rect_volume)
        pygame.draw.rect(screen, (0, 0, 0), slider_handle_volume)

    def update_slider_volume(x_position):
        nonlocal slider_handle_volume, slider_value_volume  
        if slider_rect_volume.left < x_position < slider_rect_volume.right:
            slider_handle_volume.centerx = x_position
            slider_value_volume = min_value + ((slider_handle_volume.centerx - slider_rect_volume.left) / slider_rect_volume.width) * (max_value_volume - min_value)

    running = True
    dragging_fps = False
    dragging_volume = False

    while running:
        screen.fill((255, 255, 255))
        mouse = pygame.mouse.get_pos()

        from main import font_path_title, font_path_options, height, width
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 350 < mouse[0] < 620 and 260 < mouse[1] < 310:
                        mostrar_opcoes = not mostrar_opcoes
                # Detecta se o clique foi nos sliders
                if slider_handle_fps.collidepoint(event.pos):
                    dragging_fps = True
                if slider_handle_volume.collidepoint(event.pos):
                    dragging_volume = True
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
        text_surface, surf_rect = font_path_options.render(f"Valor: {slider_value_fps:.0f}", (0, 0, 0))
        screen.blit(text_surface, (440, 400))
        fps_config, fps_rect = font_path_options.render("FPS:", (0, 0, 0))
        fps_rect = fps_config.get_rect(midleft = (width//6, height*0.5))
        screen.blit(fps_config,fps_rect)


        text_volum, volu_rect = font_path_options.render(f"Valor: {slider_value_volume:.0f}", (0, 0, 0))
        screen.blit(text_volum, (440, 550))
        vol_config, vol_rect = font_path_options.render("Volume:", (0, 0, 0))
        vol_rect = vol_config.get_rect(midleft = (width//6, height*0.7))
        screen.blit(vol_config, vol_rect)

        if mostrar_opcoes:
            for niveis in dificuldade:
                texto, texto_rect = font_path_options.render(niveis, (0, 0, 0))
                texto_rect = texto.get_rect(center=(width // 2.2, dif_padding + 135))
                pygame.draw.rect(screen, (0, 0, 0), (343, texto_rect.y - 15, 282, 47), largura_borda)
                pygame.draw.rect(screen, (255,255,255),(344,texto_rect.y-14,280,45))
                screen.blit(texto, texto_rect) 
                dif_padding += 46

        setinha_rect = setinha.get_rect(topleft = (width//2 + 70,height*0.38))
        title_config, config_rect = font_path_title.render("Configurações", (0, 0, 0))
        config_rect = title_config.get_rect(center = (width//2, height*0.12))

        dif_config, dif_rect = font_path_options.render("Dificuldade", (0, 0, 0))
        dif_rect = dif_config.get_rect(midleft = (width//6, height*0.4))

        screen.blit(title_config, config_rect)
        screen.blit(dif_config, dif_rect)
        select_dif, sel_rect = font_path_options.render(dif_sel, (0, 0, 0))
        sel_rect = select_dif.get_rect(center = (width//2.2, height*0.4))

        pygame.draw.rect(screen, (0, 0, 0), (sel_rect.x - padding - 15, sel_rect.y - padding + 15, sel_rect.width + padding * 5, sel_rect.height + padding * 1), largura_borda)
        screen.blit(select_dif, sel_rect)
        screen.blit(setinha, setinha_rect)
        dif_padding = 200
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
