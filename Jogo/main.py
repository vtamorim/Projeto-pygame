import pygame

import pygame


pygame.init()

moving_right = False
moving_left = False
class cleberson(pygame.sprite.Sprite):
    def __init__(self, x , y, scale,speed):
        self.speed = speed
        pygame.sprite.Sprite.__init__(self)
        image  = pygame.image.load('Jogo/blz.png').convert_alpha()
        self.image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        self.image_rect=  self.image.get_rect()
        self.image_rect.center = (x,y)
    def move(self,moving_left,moving_right):
        dx = 0
        dy = 0 
        
        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed

        self.image_rect.x += dx
        self.image_rect.y += dy             
    
    def draw(self):
        screen.blit(self.image,self.image_rect)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
player = cleberson(200,200,3,5)

while running:
    screen.fill((0,0,0))
    player.draw()
    player.move(moving_left,moving_right)
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            running = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_a:
                moving_left = True
            if event.type == pygame.K_d:
                moving_right = True
        if event.type == pygame.KEYUP:
            if event.type == pygame.K_a:
                moving_left = False
            if event.type == pygame.K_d:
                moving_right = False

    pygame.display.flip()

    clock.tick(60)  
pygame.quit()

    
        
