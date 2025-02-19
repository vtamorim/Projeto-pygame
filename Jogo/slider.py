import pygame
import os
import random 
import csv
pygame.init()

# Configurações da tela
screen_width = 1000
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo")

# Variáveis principais
clock = pygame.time.Clock()
Fps = 60
gravity = 0.75
Tile_size = 40

rows = 16
cols = 150
Tile_size = screen_height // rows 
tyles_tipes = 17
lvl = 1
# Controle de movimento e ações
moving_left = False
moving_right = False
attacking = False
defending = False
double_jump = False
special_attack = False
special_moving = False
original_position = None  
shoot = False

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
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
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
        self.image = self.animation_list[self.action][self.frame_index]
        if self.action in [3,4,6]:
            animation_cooldown = 50
        if self.action in [1]:
            animation_cooldown = 50
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action in [8,7]:
                len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

            # Finaliza ataques
            if self.action in [3, 4, 6]:  
                self.update_action(0)
                attacking = False  

            # Finaliza defesa

            # Finaliza ataque especial e move de volta
            if self.action == 5:  
                if special_moving:
                    self.rect.x = original_position  
                    special_moving = False  
                self.update_action(0)
                special_attack = False  

    def move(self, moving_left, moving_right):
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
    def shoot(self):
        if self.sporo_cooldown == 0:
            self.sporo_cooldown = 20  # Tempo menor para evitar travamentos
            new_sporo = Sporo(self.rect.centerx + (self.direction * self.rect.width * 0.6),
            self.rect.centery, self.direction)
            sporo_group.add(new_sporo)
    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1,200) == 1:
                #self.update_action(1) idle
                self.idling = True
                self.idling_counter = 50
            if self.vision.colliderect(player.rect):
                #self.update_action(1)
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else: 
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left,ai_moving_right)
                    self.move_counter += 1
                    #pá atualizar os zói dos musurum
                    self.vision.center = (self.rect.centerx - 75 * self.direction, self.rect.centery)
                    if self.move_counter > Tile_size:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
    def special_attack_move(self):
        global special_moving, original_position
        if not special_moving:
            original_position = self.rect.x  # Salva a posição inicial
            if self.flip: 
                self.rect.x = enemy.rect.x  # Move para trás se estiver virado
            else:
                self.rect.x = enemy.rect.x  # Move para frente se estiver normal
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
            for x,tile in enumerate(row):
                if 0 <= tile < len(img_list):
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * Tile_size
                    img_rect.y = y * Tile_size
                    tile_data = (img,img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile>= 3 and tile <= 5:
                        pass
                    elif tile == 13:
                        player = Principal('Personagem Principal', x*Tile_size, y*Tile_size, 1.65, 3)
                        health_bar = hearthbar(10,10,player.health,player.health)
                    elif tile == 14:
                        cogumelo = Principal('tileset_png/inimigo_cogumelo', x*Tile_size,y*Tile_size,0.9,1)
                        sporo_group.add(cogumelo)
                    elif tile == 8:
                        pass
                    elif tile == 16:
                        pass
        return player, health_bar
    def draw(self):
        for tile in self.obstacle_list:
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
    def __init__(self, x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = sporo
        self.rect = self.image.get_rect()
        self.rect.center =(x,y)
        self.direction = direction
    def update(self):
        self.rect.x -= (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > screen_width :
            self.kill()
        if pygame.sprite.spritecollide(player,sporo_group, False):
            if player.alive:
                player.health -= 5

                self.kill()
        #if pygame.sprite.spritecollide(player,sporo_group, False):
            #if cogumelo.alive:
                #self.kill()

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
    
print(world_data)
world = World()
player, health_bar = world.process_data(world_data)
running = True
while running:
    
    
    for enemy in sporo_group:
        enemy.updatesporo()
        enemy.draw()
    clock.tick(Fps)
    draw_bg()
    world.draw()
    health_bar.draw(player.health)
    player.update_animation()
    player.move(moving_left, moving_right)
    player.draw()
    player.updatesporo()
    
    
    sporo_group.update()
    sporo_group.draw(screen)
    if player.alive:
        if defending:
            player.update_action(7)  # Defesa
        elif special_attack:
            player.update_action(5)  # Ataque Especial
            player.special_attack_move()
        elif player.in_air:
            if player.double_jump:
                player.update_action(9)  # Pulo Duplo
            else:
                player.update_action(2)  # Pulo
        elif moving_left or moving_right:
            player.update_action(1)  # Movimento
        elif attacking:
            if player.attack_type == 1:
                player.update_action(3)  # Ataque 1
            elif player.attack_type == 2:
                player.update_action(4)  # Ataque 2
            elif player.attack_type == 3:
                player.update_action(6)  # Ataque no Pulo
        else:
            player.update_action(0)  # Parado
    else:
        player.update_action(8)
    #if cogumelo.alive == False:
        #cogumelo.update_action(8)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                defending = False
            if event.key == pygame.K_q:
                special_attack = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not attacking:  
                attacking = True
                player.attack_type = 1  
            elif event.button == 3 and not attacking:  
                attacking = True
                player.attack_type = 2  

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump = True  
            if event.key == pygame.K_s:
                defending = True
            if event.key == pygame.K_q and not special_attack:
                special_attack = False  

    pygame.display.flip()

pygame.quit()
