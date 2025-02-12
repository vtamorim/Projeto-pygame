import pygame

# Inicializa o Pygame
pygame.init()

# Definindo as dimensões da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Slider em Pygame")

# Cores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


min_value = 0
max_value = 120
slider_value = (max_value - min_value) * 0.5 
slider_rect = pygame.Rect(200, 250, 400, 10) 
slider_handle = pygame.Rect(380, 245, 20, 20) 


def draw_slider():
    pygame.draw.rect(screen, GRAY, slider_rect) 
    pygame.draw.rect(screen, RED, slider_handle)  


def update_slider(x_position):
    global slider_handle, slider_value
    if slider_rect.left < x_position < slider_rect.right:
        slider_handle.centerx = x_position
        slider_value = min_value + ((slider_handle.centerx - slider_rect.left) / slider_rect.width) * (max_value - min_value)

running = True
dragging = False

while running:
    screen.fill(WHITE)

   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if slider_handle.collidepoint(event.pos):
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                update_slider(event.pos[0])

    draw_slider()

    
    font = pygame.font.Font(None, 36)
    text = font.render(f'Valor: {slider_value:.0f}', True, BLACK)
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 300))

    # Atualizar a tela
    pygame.display.flip()

# Finalizar Pygame
pygame.quit()
