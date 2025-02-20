import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Definindo a tela
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Pausa no Pygame')

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Variáveis de controle
paused = False

# Função para desenhar a tela
def draw_game():
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (250, 150, 100, 100))

# Função de pausa
def pause_game():
    font = pygame.font.Font(None, 74)
    text = font.render("PAUSE", True, (0, 0, 0))
    screen.blit(text, (250, 150))

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Alterna o estado de pausa ao pressionar a tecla 'p'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if paused:
        pause_game()  # Exibe a tela de pausa
    else:
        draw_game()  # Desenha o jogo normalmente

    pygame.display.flip()  # Atualiza a tela
