import pygame
from pygame import mixer
import os
import random
import csv
import button
import json
music2 =pygame.mixer.Sound('audio/music2.mp3')
# Carregar conquistas do arquivo conquistas.json
with open('Conquistas/conquistas.json', 'r') as f:
    conquistas = json.load(f)

first_enemy = False
def wow(fps, volume,difficulty,medidor):
	mixer.init()
	pygame.init()


	SCREEN_WIDTH = 1000
	SCREEN_HEIGHT = int(720)

	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('Shooter')

	#set framerate
	clock = pygame.time.Clock()
	FPS = fps

	#define game variables
	GRAVITY = 0.75
	SCROLL_THRESH = 200
	ROWS = 16
	COLS = 150
	TILE_SIZE = SCREEN_HEIGHT // ROWS
	TILE_TYPES = 21
	MAX_LEVELS = 3
	screen_scroll = 0
	bg_scroll = 0
	level = 1
	start_intro = False

	first_enemy = False
	#define player action variables
	moving_left = False
	moving_right = False
	shoot = False

	def show_message(text, font, text_col, x, y):
		img = font.render(text, True, text_col)
		screen.blit(img, (x, y))


	jump_fx = pygame.mixer.Sound('audio/jump.wav')
	jump_fx.set_volume(0.05)
	shot_fx = pygame.mixer.Sound('audio/shot.wav')
	shot_fx.set_volume(0.05)



	#load images
	#button images
	start_img = pygame.image.load('img/start_btn.png').convert_alpha()
	exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
	restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
	#background
	pine1_img = pygame.image.load('tileset_png/assets-fundo/front.png').convert_alpha()
	canyon = pygame.image.load('tileset_png/assets-fundo/canyon.png').convert_alpha()
	clouds = pygame.image.load('tileset_png/assets-fundo/clouds.png').convert_alpha()
	far_moutain = pygame.image.load('tileset_png/assets-fundo/far-mountains.png').convert_alpha()
	sky = pygame.image.load('tileset_png/assets-fundo/sky.png').convert_alpha()
	sky = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
	far_moutain = pygame.transform.scale(far_moutain , (SCREEN_WIDTH - 0, SCREEN_HEIGHT - 200))
	clouds = pygame.transform.scale(clouds, (SCREEN_WIDTH - 0, SCREEN_HEIGHT - 200))
	canyon = pygame.transform.scale(canyon, (SCREEN_WIDTH - 0, SCREEN_HEIGHT - 200))
	pine1_img = pygame.transform.scale(pine1_img, (SCREEN_WIDTH - 0, SCREEN_HEIGHT - 200))


	#store tiles in a list
	img_list = []
	for x in range(TILE_TYPES):
		img = pygame.image.load(f'tileset_png/tile/{x}.png')
		img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
		img_list.append(img)
	#bullet
	bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()


	#pick up boxes
	health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
	ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()

	item_boxes = {
		'Health'	: health_box_img,
		'Ammo'		: ammo_box_img,
	}


	#define colours
	BG = (144, 201, 120)
	RED = (255, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	BLACK = (0, 0, 0)
	PINK = (235, 65, 54)

	#define font
	font = pygame.font.SysFont('Futura', 30)

	def draw_text(text, font, text_col, x, y):
		img = font.render(text, True, text_col)
		screen.blit(img, (x, y))


	def draw_bg():
		screen.fill(BG)
		width = sky.get_width()
		for x in range(5):
			screen.blit(sky, ((x * width) - bg_scroll * 0.5, 0))
			screen.blit(clouds, ((x * width) - bg_scroll * 0.6, 0))
			screen.blit(far_moutain, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - far_moutain.get_height() - 100))
			screen.blit(canyon, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - canyon.get_height() + 50))
			screen.blit(pine1_img, ((x * width) - bg_scroll * 0.9, SCREEN_HEIGHT - pine1_img.get_height() + 50))
			


	#function to reset level
	def reset_level():
		enemy_group.empty()
		bullet_group.empty()

		item_box_group.empty()
		decoration_group.empty()
		water_group.empty()
		exit_group.empty()

		#create empty tile list
		data = []
		for row in range(ROWS):
			r = [-1] * COLS
			data.append(r)

		return data




	class Soldier(pygame.sprite.Sprite):
		def __init__(self, char_type, x, y, scale, speed, ammo, ):
			pygame.sprite.Sprite.__init__(self)
			self.alive = True
			self.char_type = char_type
			self.speed = speed
			self.ammo = ammo
			self.start_ammo = ammo
			self.shoot_cooldown = 0
			self.health = 100
			self.max_health = self.health
			self.direction = 1
			self.vel_y = 0
			self.jump = False
			self.in_air = True
			self.flip = False
			self.animation_list = []
			self.frame_index = 0
			self.action = 0
			self.abates= 0
			self.update_time = pygame.time.get_ticks()
			#ai specific variables
			self.move_counter = 0
			self.vision = pygame.Rect(0, 0, 150, 20)
			self.idling = False
			self.idling_counter = 0
			
			#load all images for the players
			animation_types = ['Idle', 'Run', 'Jump', 'Death']
			for animation in animation_types:
				#reset temporary list of images
				temp_list = []
				#count number of files in the folder
				num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
				for i in range(num_of_frames):
					img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
					img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
					temp_list.append(img)
				self.animation_list.append(temp_list)

			self.image = self.animation_list[self.action][self.frame_index]
			self.rect = self.image.get_rect()
			self.rect.center = (x, y)
			self.width = self.image.get_width()
			self.height = self.image.get_height()


		def update(self):
			self.update_animation()
			self.check_alive()
			#update cooldown
			if self.shoot_cooldown > 0:
				self.shoot_cooldown -= 1


		def move(self, moving_left, moving_right):
			#reset movement variables
			screen_scroll = 0
			dx = 0
			dy = 0

			#assign movement variables if moving left or right
			if moving_left:
				dx = -self.speed
				self.flip = True
				self.direction = -1
			if moving_right:
				dx = self.speed
				self.flip = False
				self.direction = 1

			#jump
			if self.jump == True and self.in_air == False:
				self.vel_y = -13
				self.jump = False
				self.in_air = True

			#apply gravity
			self.vel_y += GRAVITY
			if self.vel_y > 10:
				self.vel_y
			dy += self.vel_y

			
			for tile in world.obstacle_list:
				
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
					
					if self.char_type == 'enemy':
						self.direction *= -1
						self.move_counter = 0
				
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				
					if self.vel_y < 0:
						self.vel_y = 0
						dy = tile[1].bottom - self.rect.top
					
					elif self.vel_y >= 0:
						self.vel_y = 0
						self.in_air = False
						dy = tile[1].top - self.rect.bottom


	
			if pygame.sprite.spritecollide(self, water_group, False):
				self.health = 0

			
			level_complete = False
			if pygame.sprite.spritecollide(self, exit_group, False):
				level_complete = True

			
			if self.rect.bottom > SCREEN_HEIGHT:
				self.health = 0


			
			if self.char_type == 'player':
				if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
					dx = 0

			
			self.rect.x += dx
			self.rect.y += dy

			
			if self.char_type == 'player':
				if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
					or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
					self.rect.x -= dx
					screen_scroll = -dx

			return screen_scroll, level_complete



		def shoot(self):
			if self.shoot_cooldown == 0 and self.ammo > 0:
				self.shoot_cooldown = 20
				bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
				bullet_group.add(bullet)
				#reduce ammo
				self.ammo -= 1
				shot_fx.play()


		def ai(self):
			if self.alive and player.alive:
				if self.idling == False and random.randint(1, 200) == 1:
					self.update_action(0)#0: idle
					self.idling = True
					self.idling_counter = 50
				
				if self.vision.colliderect(player.rect):
					
					self.update_action(0)
					
					self.shoot()
				else:
					if self.idling == False:
						if self.direction == 1:
							ai_moving_right = True
						else:
							ai_moving_right = False
						ai_moving_left = not ai_moving_right
						self.move(ai_moving_left, ai_moving_right)
						self.update_action(1)#1: run
						self.move_counter += 1
						#update ai vision as the enemy moves
						self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

						if self.move_counter > TILE_SIZE:
							self.direction *= -1
							self.move_counter *= -1
					else:
						self.idling_counter -= 1
						if self.idling_counter <= 0:
							self.idling = False

			#scroll
			self.rect.x += screen_scroll


		def update_animation(self):
			#update animation
			ANIMATION_COOLDOWN = 100
			#update image depending on current frame
			self.image = self.animation_list[self.action][self.frame_index]
			#check if enough time has passed since the last update
			if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
				self.update_time = pygame.time.get_ticks()
				self.frame_index += 1
			#if the animation has run out the reset back to the start
			if self.frame_index >= len(self.animation_list[self.action]):
				if self.action == 3:
					self.frame_index = len(self.animation_list[self.action]) - 1
				else:
					self.frame_index = 0



		def update_action(self, new_action):
			#check if the new action is different to the previous one
			if new_action != self.action:
				self.action = new_action
				#update the animation settings
				self.frame_index = 0
				self.update_time = pygame.time.get_ticks()



		def check_alive(self):
			global first_enemy
			if self.health <= 0:
				self.health = 0
				self.speed = 0
				self.alive = False
				self.update_action(3)
				if self.char_type == 'enemy' and first_enemy == False:
					first_enemy = True
				


		def draw(self):
			screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


	class World():
		def __init__(self):
			self.obstacle_list = []

		def process_data(self, data):
			self.level_length = len(data[0])
			#iterate through each value in level data file
			for y, row in enumerate(data):
				for x, tile in enumerate(row):
					if tile >= 0:
						img = img_list[tile]
						img_rect = img.get_rect()
						img_rect.x = x * TILE_SIZE
						img_rect.y = y * TILE_SIZE
						tile_data = (img, img_rect)
						if tile >= 0 and tile <= 8:
							self.obstacle_list.append(tile_data)
						elif tile >= 9 and tile <= 10:
							water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
							water_group.add(water)
						elif tile >= 11 and tile <= 14:
							decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
							decoration_group.add(decoration)
						elif tile == 15:#create player
							player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 20)
							health_bar = HealthBar(10, 10, player.health, player.health)
						elif tile == 16:#create enemies
							enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20)
							enemy_group.add(enemy)
						elif tile == 17:#create ammo box
							item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
							item_box_group.add(item_box)
						elif tile == 19:#create health box
							item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
							item_box_group.add(item_box)
						elif tile == 20:#create exit
							exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
							exit_group.add(exit)

			return player, health_bar


		def draw(self):
			for tile in self.obstacle_list:
				tile[1][0] += screen_scroll
				screen.blit(tile[0], tile[1])


	class Decoration(pygame.sprite.Sprite):
		def __init__(self, img, x, y):
			pygame.sprite.Sprite.__init__(self)
			self.image = img
			self.rect = self.image.get_rect()
			self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

		def update(self):
			self.rect.x += screen_scroll


	class Water(pygame.sprite.Sprite):
		def __init__(self, img, x, y):
			pygame.sprite.Sprite.__init__(self)
			self.image = img
			self.rect = self.image.get_rect()
			self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

		def update(self):
			self.rect.x += screen_scroll

	class Exit(pygame.sprite.Sprite):
		def __init__(self, img, x, y):
			pygame.sprite.Sprite.__init__(self)
			self.image = img
			self.rect = self.image.get_rect()
			self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

		def update(self):
			self.rect.x += screen_scroll


	class ItemBox(pygame.sprite.Sprite):
		def __init__(self, item_type, x, y):
			pygame.sprite.Sprite.__init__(self)
			self.item_type = item_type
			self.image = item_boxes[self.item_type]
			self.rect = self.image.get_rect()
			self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


		def update(self):
			#scroll
			self.rect.x += screen_scroll
			#check if the player has picked up the box
			if pygame.sprite.collide_rect(self, player):
				#check what kind of box it was
				if self.item_type == 'Health':
					player.health += 25
					if player.health > player.max_health:
						player.health = player.max_health
				elif self.item_type == 'Ammo':
					player.ammo += 15
				#delete the item box
				self.kill()


	class HealthBar():
		def __init__(self, x, y, health, max_health):
			self.x = x
			self.y = y
			self.health = health
			self.max_health = max_health

		def draw(self, health):
			#update with new health
			self.health = health
			#calculate health ratio
			ratio = self.health / self.max_health
			pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
			pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
			pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


	class Bullet(pygame.sprite.Sprite):
		def __init__(self, x, y, direction):
			pygame.sprite.Sprite.__init__(self)
			self.speed = 10
			self.image = bullet_img
			self.rect = self.image.get_rect()
			self.rect.center = (x, y)
			self.direction = direction

		def update(self):
			#move bullet
			self.rect.x += (self.direction * self.speed) + screen_scroll
			#check if bullet has gone off screen
			if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
				self.kill()
			#check for collision with level
			for tile in world.obstacle_list:
				if tile[1].colliderect(self.rect):
					self.kill()

			#check collision with characters
			if pygame.sprite.spritecollide(player, bullet_group, False):
				if player.alive:
					if difficulty == 'Médio':
						player.health -= 10
					elif difficulty == 'Difícil':
						player.health -= 15
					elif difficulty == 'Fácil':
						player.health -= 5
					self.kill()
			for enemy in enemy_group:
				if pygame.sprite.spritecollide(enemy, bullet_group, False):
					if enemy.alive:
						if difficulty == 'Médio':
							enemy.health -= 30
						elif difficulty == 'Difícil':
							enemy.health -= 25
						elif difficulty == 'Fácil':
							enemy.health -= 20
						self.kill()






	class ScreenFade():
		def __init__(self, direction, colour, speed):
			self.direction = direction
			self.colour = colour
			self.speed = speed
			self.fade_counter = 0


		def fade(self):
			fade_complete = False
			self.fade_counter += self.speed
			if self.direction == 1:#whole screen fade
				pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
				pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
				pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
				pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 +self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
			if self.direction == 2:#vertical screen fade down
				pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
			if self.fade_counter >= SCREEN_WIDTH:
				fade_complete = True

			return fade_complete


	#create screen fades
	intro_fade = ScreenFade(1, BLACK, 4)
	death_fade = ScreenFade(2, PINK, 4)


	#create buttons
	start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
	exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
	restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

	#create sprite groups
	enemy_group = pygame.sprite.Group()
	bullet_group = pygame.sprite.Group()


	item_box_group = pygame.sprite.Group()
	decoration_group = pygame.sprite.Group()
	water_group = pygame.sprite.Group()
	exit_group = pygame.sprite.Group()



	#create empty tile list
	world_data = []
	for row in range(ROWS):
		r = [-1] * COLS
		world_data.append(r)
	#load in level data and create world
	with open(f'level{level}_data.csv', newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for x, row in enumerate(reader):
			for y, tile in enumerate(row):
				world_data[x][y] = int(tile)
	world = World()
	player, health_bar = world.process_data(world_data)



	run = True
	while run:
		medidor = 0.03
		music2.set_volume(medidor)
		music2.play()
		def verificar_conquistas():
			global first_enemy
			for conquista in conquistas:
				if conquista['condicao'] == 'primeiro_inimigo' and first_enemy:
					show_message(conquista['mensagem'], font, RED, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
		clock.tick(FPS)

		if True:
			#update background
			draw_bg()
			#draw world map
			world.draw()
			#show player health
			health_bar.draw(player.health)
			#show ammo

			
			# Verificar e exibir conquistas
			verificar_conquistas()

			player.update()
			player.draw()

			for enemy in enemy_group:
				enemy.ai()
				enemy.update()
				enemy.draw()

			#update and draw groups
			bullet_group.update()

			item_box_group.update()
			decoration_group.update()
			water_group.update()
			exit_group.update()
			bullet_group.draw(screen)

		
			item_box_group.draw(screen)
			decoration_group.draw(screen)
			water_group.draw(screen)
			exit_group.draw(screen)

			#show intro
			if start_intro == True:
				if intro_fade.fade():
					start_intro = False
					intro_fade.fade_counter = 0


			#update player actions
			if player.alive:
				#shoot bullets
				if shoot:
					player.shoot()
				if player.in_air:
					player.update_action(2)#2: jump
				elif moving_left or moving_right:
					player.update_action(1)#1: run
				else:
					player.update_action(0)#0: idle
				screen_scroll, level_complete = player.move(moving_left, moving_right)
				bg_scroll -= screen_scroll
				#check if player has completed the level
				if level_complete:
					start_intro = True
					level += 1
					bg_scroll = 0
					world_data = reset_level()
					if level <= MAX_LEVELS:
						#load in level data and create world
						with open(f'level{level}_data.csv', newline='') as csvfile:
							reader = csv.reader(csvfile, delimiter=',')
							for x, row in enumerate(reader):
								for y, tile in enumerate(row):
									world_data[x][y] = int(tile)
						world = World()
						player, health_bar = world.process_data(world_data)	
					

						
			else:
				screen_scroll = 0
				if death_fade.fade():
					if restart_button.draw(screen):
						death_fade.fade_counter = 0
						start_intro = True
						bg_scroll = 0
						world_data = reset_level()
						#load in level data and create world
						with open(f'level{level}_data.csv', newline='') as csvfile:
							reader = csv.reader(csvfile, delimiter=',')
							for x, row in enumerate(reader):
								for y, tile in enumerate(row):
									world_data[x][y] = int(tile)
						world = World()
						player, health_bar = world.process_data(world_data)


		for event in pygame.event.get():
			#quit game
			if event.type == pygame.QUIT:
				run = False
			#keyboard presses
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					moving_left = True
				if event.key == pygame.K_d:
					moving_right = True
				if event.key == pygame.K_SPACE:
					shoot = True
				if event.key == pygame.K_w and player.alive:
					player.jump = True
					jump_fx.play()
				if event.key == pygame.K_ESCAPE:
					run = False


			#keyboard button released
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					moving_left = False
				if event.key == pygame.K_d:
					moving_right = False
				if event.key == pygame.K_SPACE:
					shoot = False


		pygame.display.update()

	pygame.quit()

