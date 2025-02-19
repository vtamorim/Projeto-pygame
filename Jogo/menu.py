import pygame
import pygame.freetype
import csv
import os
import random
import game
# Inicializando Pygame e FreeType
pygame.init()
pygame.freetype.init() 

width, height = 1000, 720
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

font_path_title = pygame.freetype.Font('Jogo/PixelifySans-VariableFont_wght.ttf', 50)
font_path_options = pygame.freetype.Font('Jogo/PixelifySans-VariableFont_wght.ttf', 25)


def menu(screen, font_path_title, font_path_options, clock,slider_value_fps,slider_handle_volume):

    running = True
    while running:
        screen.fill((255, 255, 255))
        mouse = pygame.mouse.get_pos()

        title_surface, titlerect = font_path_title.render("Lâmina Fúngica", (0, 0, 0))
        titlerect = title_surface.get_rect(center=(500, 100))
        screen.blit(title_surface, titlerect)

        # Botões
        first_option, first_option_rect = font_path_options.render("Iniciar", (0, 0, 0))
        first_option_rect = first_option.get_rect(center=(500, 300))
        screen.blit(first_option, first_option_rect)

        second_option, second_option_rect = font_path_options.render("Configurações", (0, 0, 0))
        second_option_rect = second_option.get_rect(center=(500, 400))
        screen.blit(second_option, second_option_rect)

        three_option, three_option_rect = font_path_options.render("Sair", (0, 0, 0))
        three_option_rect = three_option.get_rect(center=(500, 500))
        screen.blit(three_option, three_option_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if first_option_rect.collidepoint(mouse):
                        game() 
                    elif second_option_rect.collidepoint(mouse):
                        config(screen, font_path_title, font_path_options, clock)  # Chama config()
                    elif three_option_rect.collidepoint(mouse):
                        running = False  

        clock.tick(60)

def config(screen, font_path_title, font_path_options, clock):
    def mostrar_opcoes():
        pygame.display.set_caption("Opções")
    dificuldade = ['Fácil', 'Médio', 'Difícil']
    dif_sel = "Selecionar"
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
        arrow = pygame.transform.scale(pygame.image.load("Jogo/arrow.png"),(30,30))
        arrow_rect = arrow.get_rect(topleft = (0,0))
        
        
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
                if arrow_rect.collidepoint(mouse):
                    menu(screen, font_path_title, font_path_options, clock, slider_value_fps,slider_handle_volume,dif_config)
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

        text_surface, _ = font_path_options.render(f"Valor: {slider_value_fps:.0f}", (0, 0, 0))
        screen.blit(text_surface, (440, 400))
        fps_config, fps_rect = font_path_options.render("FPS:", (0, 0, 0))
        fps_rect = fps_config.get_rect(midleft = (width//6, height*0.5))
        screen.blit(fps_config,fps_rect)


        text_volum,_ = font_path_options.render(f"Valor: {slider_value_volume:.0f}", (0, 0, 0))
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if texto_rect.collidepoint(mouse):
                            mostrar_opcoes = False
                            dif_sel = str(niveis)

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
        
        screen.blit(arrow,arrow_rect)
        
       
        pygame.display.flip()
        clock.tick(60)

    mostrar_opcoes()

def game():
    global special_moving, original_position  # Add original_position to global
    clock = pygame.time.Clock()
    Fps = 60
    gravity = 0.75
    Tile_size = 40
    scool_th = 200
    rows = 16
    cols = 150
    Tile_size = height // rows
    tyles_tipes = 17
    lvl = 2
    screen_scroll = 0
    bg_scroll = 0
    original_position = 0  # Initialize original_position
    # Controle de movimento e ações
    moving_left = False
    moving_right = False
    attacking = False
    defending = False
    double_jump = False
    special_attack = False
    special_moving = False  # Initialize special_moving
    shoot = False
    speed = 3
    jump_fight = False
    run_speed = 6  # Speed when running
    running = False  # Track if the player is running

    #4 imagens
    tree_1img =pygame.image.load('tileset_png/assets-fundo/trees.png').convert_alpha()
    tree_2img =pygame.image.load('tileset_png/assets-fundo/trees1.png').convert_alpha()
    far_clouds = pygame.image.load('tileset_png/assets-fundo/far-clouds.png').convert_alpha()
    near_clods = pygame.image.load('tileset_png/assets-fundo/near-clouds.png').convert_alpha()
    far_moutain = pygame.image.load('tileset_png/assets-fundo/far-mountains.png').convert_alpha()
    mountain = pygame.image.load('tileset_png/assets-fundo/mountains.png').convert_alpha()
    sky = pygame.image.load('tileset_png/assets-fundo/sky.png').convert_alpha()
    sky = pygame.transform.scale(sky,(width,height))
    mountain = pygame.transform.scale(mountain,(width,height))
    far_moutain = pygame.transform.scale(far_moutain,(width,height))
    far_clouds = pygame.transform.scale(far_clouds,(width,height +90))
    near_clods = pygame.transform.scale(near_clods,(610,550))
    tree_1img = pygame.transform.scale(tree_1img,(width,height))
    tree_2img = pygame.transform.scale(tree_2img, (width,height - 100))
    img_list = []
    for x in range(tyles_tipes):
        img = pygame.image.load(f'tileset_png/tile/{x}.png')
        img = pygame.transform.scale(img,(Tile_size, Tile_size))
        img_list.append(img)

    sporo = pygame.transform.scale(pygame.image.load('tileset_png/ball_sporo.png').convert_alpha(), (8,8))
    BG = (144, 201, 120)
    red = (255, 0, 0)
    def draw_bg():
        screen.fill(BG)
        screen.blit(sky,(0,0))
        screen.blit(far_moutain,(0,0))
        screen.blit(near_clods,(0,0))
        screen.blit(far_clouds,(0,0))
        
        screen.blit(mountain,(0,height - mountain.get_height() - 40))
        screen.blit(tree_1img,(0,height -tree_1img.get_height() - 20))
        screen.blit(tree_2img,(0,height - tree_2img.get_height()))
        #height - tree_2img.get_height() - 50
        
        
    class Principal(pygame.sprite.Sprite):
        def __init__(self, char_type, x, y, scale, speed):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.char_type = char_type
            self.speed = speed
            self.sporo_cooldown = 0 
            self.direction = 1
            self.jump = False
            self.health = 100
            self.max_health= 100
            self.double_jump = False
            self.in_air = False
            self.vel_y = 0
            self.flip = False
            self.attack_type = 1
            self.action = 0
            self.defending = defending
            self.animation_list = []
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.move_counter = 0
            self.idling = False
            self.idling_counter = 0
            self.jump_fight = jump_fight
            self.vision = pygame.Rect(0,0,150,20)
            # Lista de animações
            self.animation_types = [
                'Parado', 'Flutuo', 'Pulo', 'Ataque 1', 'Ataque 2', 'Ataque Especial',
                'Ataque no Pulo', 'Defesa', 'Morte', 'Pulo Duplo', 'Sofrendo Dano'
            ]
            
            for animation in self.animation_types:
                temp_list = []
                animation_path = f'{char_type}/{animation}'
                if os.path.exists(animation_path):
                    num_of_frames = len(os.listdir(animation_path))
                    for i in range(num_of_frames):        
                        img = pygame.image.load(f"{animation_path}/{i}.png")
                        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale))).convert_alpha()
                        temp_list.append(img)    
                    self.animation_list.append(temp_list) 

                    

            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.width = self.image.get_width()
            self.height = self.image.get_height()    
        def updatesporo(self):
            self.update_animation()
            self.check_alive()
            if self.sporo_cooldown > 0:
                self.sporo_cooldown -= 1
        def update_animation(self):
            global attacking, defending, special_attack, special_moving

            animation_cooldown = 100  
            if self.action < len(self.animation_list) and self.animation_list[self.action]:
                self.image = self.animation_list[self.action][self.frame_index]
            if self.action in [3, 4, 6]:
                animation_cooldown = 50
            if self.action in [1]:
                animation_cooldown = 50
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1

            if self.action < len(self.animation_list) and self.frame_index >= len(self.animation_list[self.action]):
                if self.action in [8, 7, 1]:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

                if self.action in [3, 4, 6]:  
                    self.update_action(0)
                    attacking = False  

                if self.action == 5:  
                    if special_moving:
                        self.rect.x = original_position  
                        special_moving = False 
                        special_attack = False   
                    self.update_action(0)
                    

        def move(self, moving_left, moving_right):
            screen_scroll  = 0
            dx = 0
            dy = 0
            if moving_left:
                dx = -self.speed
                self.flip = True
            if moving_right:
                dx = self.speed
                self.flip = False

            # Pulo e Pulo Duplo
            if self.jump:
                if not self.in_air:
                    self.vel_y = -11
                    self.in_air = True
                    self.double_jump = True
                    self.update_action(2)  # Animação de Pulo
                elif self.double_jump:  
                    self.vel_y = -11
                    self.double_jump = False
                    self.update_action(9)  # Animação de Pulo Duplo
                if self.jump_fight:
                    self.update_action(6)
                    self.jump_fight = False
                self.jump = False

            self.vel_y += gravity
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Verifica se está no chão
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect.x+dx, self.rect.y,self.width,self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0 :
                        self.vel_y  = 0
                        dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom
                        


            self.rect.x += dx
            self.rect.y += dy

            if self.char_type == 'Personagem Principal':
                if self.rect.right > screen.get_width() - scool_th or self.rect.left < scool_th:
                    self.rect.x  -= dx
                    screen_scroll = -dx
            return screen_scroll 
            
        def ai(self):
            if self.alive and player.alive:
                if self.idling == False and random.randint(1, 200) == 1:
                    self.idling = True
                    self.idling_counter = 50
                if self.vision.colliderect(player.rect):
                    self.update_action(1)  # Idle animation
                    if self.sporo_cooldown == 0:
                        self.shoot()  # Atira um sporo
                else:
                    if self.idling == False:
                        if self.direction == 1:
                            ai_moving_right = True
                        else:
                            ai_moving_right = False
                        ai_moving_left = not ai_moving_right
                        self.move(ai_moving_left, ai_moving_right)
                        self.move_counter += 1
                        self.vision.center = (self.rect.centerx - 75 * self.direction, self.rect.centery)
                        if self.move_counter > Tile_size:
                            self.direction *= -1
                            self.move_counter *= -1
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False
            self.rect.x += screen_scroll

        def shoot(self):
            if self.sporo_cooldown == 0:
                self.sporo_cooldown =5 # Cooldown para o próximo disparo
                new_sporo = Sporo(self.rect.centerx + (self.direction * self.rect.width * 0.6),
                                self.rect.centery, self.direction)
                sporo_group.add(new_sporo)

        def special_attack_move(self):
            global special_moving, original_position  
            if not special_moving:
                original_position = self.rect.x 
                if self.flip: 
                    self.rect.x = cogumelo.rect.x 
                else:
                    self.rect.x =cogumelo.rect.x 
                special_moving = True  

        def update_action(self, new_action):
            if new_action != self.action:
                self.action = new_action
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()
        def check_alive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                
        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    class World():
        def __init__(self):
            self.obstacle_list = []

        def process_data(self, data):
            player = None
            for y, row in enumerate(data):
                for x, tile in enumerate(row):
                    if 0 <= tile < len(img_list):
                        img = img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * Tile_size
                        img_rect.y = y * Tile_size
                        tile_data = (img, img_rect)
                        if tile >= 0 and tile <= 8:
                            self.obstacle_list.append(tile_data)
                        elif tile >= 3 and tile <= 5:
                            pass
                        elif tile == 13:
                            player = Principal('Personagem Principal', x * Tile_size, y * Tile_size, 1.65, 3)
                            health_bar = hearthbar(10, 10, player.health, player.health)
                        elif tile == 14:
                            cogumelo = Principal('tileset_png/inimigo_cogumelo', x * Tile_size + 35, y * Tile_size + 30, 0.9, 1)
                            cogumelo_group.add(cogumelo)  # Adicione o cogumelo ao grupo
                        elif tile == 8:
                            pass
                        elif tile == 16:
                            pass
            return player, health_bar
        def draw(self):
            for tile in self.obstacle_list:
                tile [1][0] += screen_scroll
                screen.blit(tile[0],tile[1])
    #class Exit (pygame.sprite.Sprite):
        #def __init__(self, img,x,y):
            #pygame.sprite.Sprite.__init__(self)
            #self.rect = self.image.get_rect()
            #self.rect.midtop = (x+Tile_size//2, y (tyles_tipes - self.image.get_height()))
    class Decoration(pygame.sprite.Sprite):
        def __init__(self, item_type, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image =img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x+Tile_size//2, y (tyles_tipes - self.image.get_height()))
    class Sporo(pygame.sprite.Sprite):
        def __init__(self, x, y, direction, principal):
            pygame.sprite.Sprite.__init__(self)
            self.speed = 10
            self.image = sporo
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction
            self.principal = principal 
            
        def update(self):
            self.rect.x -= (self.direction * self.speed)
            if self.rect.right < 0 or self.rect.left > width:
                self.kill()

            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect):
                    self.kill()

            if pygame.sprite.spritecollide(player, sporo_group, False):
                if player.alive and defending == False:
                    player.health -= 5
                    self.kill()

        def updatesporo(self):
            
            self.principal.update_animation()  
            self.principal.check_alive()  
            if self.principal.sporo_cooldown > 0:
                self.principal.sporo_cooldown -= 1

        def __init__(self, x,y,direction):
            pygame.sprite.Sprite.__init__(self)
            self.speed = 10
            self.image = sporo
            self.rect = self.image.get_rect()
            self.rect.center =(x,y)
            self.direction = direction
            self.principal = Principal
        def update(self):
            self.rect.x -= (self.direction * self.speed)
            if self.rect.right < 0 or self.rect.left > width :
                self.kill()
            
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect):
                    self.kill()
            if pygame.sprite.spritecollide(player,sporo_group, False):
                if player.alive:
                    player.health -= 5

                    self.kill()
            #if pygame.sprite.spritecollide(player,sporo_group, False):
                #if cogumelo.alive:
                    #self.kill()
        def updatesporo(self):
            self.principal.update_animation(self)
            self.principal.check_alive(self)
            
            if self.principal.sporo_cooldown > 0:
                self.sporo_cooldown -= 1
            

    cogumelo_group = pygame.sprite.Group()
    sporo_group = pygame.sprite.Group()
    item_box_group = pygame.sprite.Group()
    exit_group = pygame.sprite.Group()
    class hearthbar():

        def __init__(self,x,y,health,max_health):
            self.x  = x
            self.y = y
            self.health = health
            self.max_health = max_health
        def draw(self,health):
            self.health = health
            ratio = self.health / self.max_health   
            pygame.draw.rect(screen,(0,0,0), (self.x - 2, self.y - 2, 150,20))
            pygame.draw.rect(screen,red, (self.x,self.y, 150, 20))
            pygame.draw.rect(screen,(0,255,0),(self.x,self.y,150 * ratio, 20))


    world_data = []
    for row in range(rows):
        r = [-1] * cols
        world_data.append(r)
    with open(f'level{lvl}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x,row in enumerate(reader):
            for y,tile in enumerate(row):
                world_data[x][y] = int(tile)
        

    world = World()
    player, health_bar = world.process_data(world_data)
    running = True
    while running:
        clock.tick()
        draw_bg()
        world.draw()
        health_bar.draw(player.health)
        player.update_animation()
        screen_scroll = player.move(moving_left, moving_right)
        player.draw()

        # Atualize e desenhe os inimigos cogumelos
        for cogumelo in cogumelo_group:
            cogumelo.ai()
            cogumelo.update_animation()
            cogumelo.draw()

        sporo_group.update()
        sporo_group.draw(screen)

        if player.alive:
            if defending:
                player.update_action(7)  # Defesa
            elif special_attack:
                player.update_action(5)  # Ataque Especial
                player.special_attack_move()  # Move o personagem para o cogumelo
            elif attacking:
                player.update_action(3)  # Ataque 1
            elif moving_left or moving_right:
                player.update_action(1)  # Flutuo
            else:
                player.update_action(0)  # Parado

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w and player.alive:
                    player.jump = True
                if event.key == pygame.K_SPACE:
                    attacking = True
                if event.key == pygame.K_s:
                    defending = True
                if event.key == pygame.K_e:
                    special_attack = False
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    speed = 6
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not attacking:
                    attacking = True
                    player.attack_type = 1
                elif event.button == 3 and not attacking:
                    attacking = True
                    player.attack_type = 2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_s:
                    defending = False
                if event.key == pygame.K_SPACE:
                    attacking = False
                if event.key == pygame.K_e:
                    special_attack = True
                if event.key == pygame.K_f and player.jump:
                    player.jump_fight = True
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    speed = 6

        # Adjust speed based on running state
        player.speed = run_speed if running else speed
        if player.rect.y >= height + 900:
            player.health = 0
        pygame.display.update()

menu(screen, font_path_title, font_path_options, clock) 