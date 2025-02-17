import pygame
import os

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

# Controle de movimento e ações
moving_left = False
moving_right = False
attacking = False
defending = False
double_jump = False
special_attack = False
special_moving = False
original_position = None  

BG = (144, 201, 120)
red = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, red, (0, 300), (screen_width, 300))

class Principal(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.double_jump = False
        self.in_air = False
        self.vel_y = 0
        self.flip = False
        self.attack_type = 1
        self.action = 0
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Lista de animações
        self.animation_types = [
            'Parado', 'Flutuo', 'Pulo', 'Ataque 1', 'Ataque 2', 'Ataque Especial',
            'Ataque no Pulo', 'Defesa', 'Morte', 'Pulo Duplo', 'Sofrendo Dano'
        ]
        
        for animation in self.animation_types:
            temp_list = []
            animation_path = f'Personagem Principal/{animation}'
            if os.path.exists(animation_path):
                num_of_frames = len(os.listdir(animation_path))
                for i in range(num_of_frames):        
                    img = pygame.image.load(f"{animation_path}/{i}.png")
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)    
                self.animation_list.append(temp_list) 
                
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_animation(self):
        global attacking, defending, special_attack, special_moving

        animation_cooldown = 100  
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

            # Finaliza ataques
            if self.action in [3, 4, 6]:  
                self.update_action(0)
                attacking = False  

            # Finaliza defesa
            if self.action == 7:  
                self.update_action(0)
                defending = False

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
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def special_attack_move(self):
        global special_moving, original_position
        if not special_moving:
            original_position = self.rect.x  # Salva a posição inicial
            if self.flip:
                self.rect.x -= 100  # Move para trás se estiver virado
            else:
                self.rect.x += 100  # Move para frente se estiver normal
            special_moving = True  

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player = Principal(0, 200, 200, 3, 5)

running = True
while running:
    clock.tick(Fps)
    draw_bg()

    player.update_animation()

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

    player.move(moving_left, moving_right)
    player.draw()

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
                special_attack = False  

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
                special_attack = True  

    pygame.display.flip()

pygame.quit()
