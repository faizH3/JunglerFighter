import pygame
from spreetsheet import*
from get_image import*
import random

pygame.init()

#################### GRAVITY ######################
GRAVITY = 0.74
ROWS = 16
COLS = 150
TILE_TYPES = 21
level = 1
################## SCREEN SIZE #######################3
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

TILE_SIZE = SCREEN_HEIGHT // ROWS
####################### SCREEN SETUP ########################
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
###############################################
clock = pygame.time.Clock()
FPS = 60
##################### LOAD IMAGE ##########################


####################### COLORS ########################
GREEN = (0, 255, 0)
RED = (255, 0, 0)


###################### FONT #########################
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

################## MOVE #######################
move_left = False
move_right = False
jump = False
shoot = False
# attack  = False


bullet_img = pygame.image.load(f"img/Explosion/7.png")

# load images
# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

class Attack(pygame.sprite.Sprite):
	def __init__(self, char, x, y, direction, speed, gLeft, gRight):
		pygame.sprite.Sprite.__init__(self)
		self.char = char
		self.action = 3
		self.speed = speed
		self.frame_index = 0
		self.image = self.char[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.update_time = pygame.time.get_ticks()
		self.direction = direction

	def update(self):
		self.rect.x += (self.direction*self.speed)
		print(self.rect.x)
		self.image = self.char[self.action][self.frame_index]
		if pygame.time.get_ticks() - self.update_time > 100:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		if self.frame_index >= len(self.char[self.action]):
			self.frame_index = 0
			self.kill()
		


################## CLASS OBJECT ########################
class Character(pygame.sprite.Sprite):
	def __init__(self, char, x, y, speed, ammo):
		pygame.sprite.Sprite.__init__(self)
		self.idling = False
		self.idling_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20)
		self.move_counter = 0
		self.char = char
		self.speed = speed
		self.alive = True
		self.flip = False
		self.attack = False
		self.in_air = True
		self.jump = False
		self.ammo = ammo
		self.direction = 1
		self.shoot_cooldown = 0
		self.health = 100
		self.max_health = self.health
		self.vel_y = 0
		self.frame_index = 0
		self.action = 0
		self.image = self.char[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.update_time = pygame.time.get_ticks()

	def update(self):
		self.update_animation()
		self.check_alive()
		# self.attack()
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1

	def move(self, move_left, move_right):
		dx = 0
		dy = 0
		if move_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if move_right:
			dx = self.speed
			self.flip = False
			self.direction = 1
		if self.jump == True and self.in_air == False:
			self.vel_y = -11
			self.jump = False
			self.in_air = True
		
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y
		
		if self.rect.bottom  + dy > 610:
			dy = 610 - self.rect.bottom
			self.in_air = False
		
		self.rect.x += dx
		self.rect.y += dy
		
	def update_animation(self):
		ANIMATION_COOLDOWN = 100
		self.image = self.char[self.action][self.frame_index]
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		if self.frame_index >= len(self.char[self.action]):
			# if self.action == 3:
			# 	self.frame_index = len(self.char[self.action]) - 1
			# else:
			self.frame_index = 0

	def attacker(self):
		aAttack = Attack(self.char, self.rect.centerx, self.rect.centery, self.direction, self.speed)
		aAttack_group.add(aAttack)
	
	def frame_attacks(self, a, b):
		# player.update_action(3)
		self.action = a
		# self.frame_index = b
		
		if pygame.time.get_ticks() - self.update_time > 10:
			self.update_time = pygame.time.get_ticks()
			for y in  range(1, b):
				self.image = self.char[self.action][y]
				return self.image

		
	def update_action(self, new_action):
		if new_action !=  self.action:
			self.action = new_action
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()
	
	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			# self.update_action(3)
	
	def shoot(self):
		# if shoot == True:
		explosion = Explosion(self.rect.centerx, self.rect.centery, 0.5, 2, self.direction, self.speed)
		print(self.rect.x)
		explosion_group.add(explosion)

	def ai(self, a, b):
		if self.alive and player.alive:
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0)
				self.idling = True
				self.idling_counter = 50
			# check if the ai in near the player
			if self.vision.colliderect(player.rect):
				# stop running and face the player
				# self.update_action(0)
				# self.update_action(1)
				self.action = a		
				if pygame.time.get_ticks() - self.update_time > 1000:
					self.update_time = pygame.time.get_ticks()
					for y in  range(1, b):
						self.image = self.char[self.action][y]
						return self.image
				# self.update_action(0)
				# if pygame.time.get_ticks() - self.update_time > 500:
				# 	self.attacker()
			else:
				if self.idling == False:
					if self.direction == 1:
						ai_move_right = True
					else:
						ai_move_right = False
					ai_move_left = not ai_move_right
					self.move(ai_move_left, ai_move_right)
					self.update_action(1)
					self.move_counter += 1
					# update ai vision as the enemy moves
					self.vision.center = (self.rect.centerx, self.rect.centery)
					if self.move_counter > TILE_SIZE:
						self.direction *= -1
						self.move_counter *= -1
				else:
					self.idling_counter -= 1
					if self.idling_counter <= 0:
						self.idling = False
	
	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		# iterate through each value in level data file
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
						water = water(img, x * TILE_SIZE, y * TILE_SIZE)
						water_group.add(water)
					elif tile >= 11 and tile <= 14:
						decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
						decoration_group.add(decoration)
					elif tile == 15: # create player
						player = Character(all_action, TILE_SIZE, y * TILE_SIZE, 1, 100)
					elif tile == 16: # create enemies
						enemy = Character(all_action, x * TILE_SIZE, y * TILE_SIZE, 1, 100)
						enemy_group.add(enemy)
					# elif tile == 17: # create ammo box
					# 	item_box = ItemBox('ammo', x  * TILE_SIZE, y * TILE_SIZE)
					# 	item_box_group.add(item_box)
					# elif tile == 18: # create grenade box
					# 	item_box = ItemBox('grenade', x * TILE_SIZE, y * TILE_SIZE)
					# 	item_box_group.add(item_box)
					# elif tile == 19: # create health box
					# 	item_box = ItemBox('health', x * TILE_SIZE, y * TILE_SIZE)
					# 	item_box_group.add(item_box)
					# elif tile == 20: # create exit
					# 	exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
					# 	exit_group.add(exit)
		return player, health_bar
	
	def draw(self):
		for tile in self.obstacle_list:
			screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x+TILE_SIZE // 2, y+(TILE_SIZE - self.image.get_height()))

class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		#check if the player has picked up the box
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 15
			elif self.item_type == 'Grenade':
				player.grenades += 3
			#delete the item box
			self.kill()

#################### HEALTH BAR ###########################
class healthBar(pygame.sprite.Sprite):
	def __init__(self, x, y, health, max_health):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health
	
	def draw(self, health):
		# update new health
		self.health = health

		# calculate health ratio
		ratio = self.health/self.max_health
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, RED, (self.x, self.y, 150*ratio, 20))

########################## BACKGROUND ##############################
bgImages = []

for i in range(0, 12):
	bg_image = pygame.image.load(f"Background/{i}.png")
	bgImages.append(bg_image)
bg_width = bgImages[i].get_width()

def draw_bg():
	for x in range(0, 12):
		speed = 2
		for i in bgImages:
			screen.blit(i, ((x*bg_width - scroll*speed), -120))
			speed += 1


########################################################
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, scale):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = bullet_img
		self.image = pygame.transform.scale(self.image, (self.image.get_width()*scale, self.image.get_height()*scale))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction
	def update(self):
		self.rect.x += (self.direction * self.speed)
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			# self.kill()
			print()
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 0
				# self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, scale_x, scale_y, direction, speed):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 7):
			img = pygame.image.load(f'img/3/{num}.png')
			img = pygame.transform.scale(img, (img.get_width()*scale_x, img.get_height()*scale_y))
			self.images.append(img)
		self.frame_index = 0
		self.speed = speed
		self.image = self.images[self.frame_index]
		self.rect = self.image.get_rect()
		x+=(direction*30)
		y+=-20
		self.rect.center = (x, y)
		self.counter = 0
		self.counter1 = 0
		self.direction = direction
	
	def update(self):
		EXPLOSION_SPEED = 1
		self.counter += 1
		self.rect.x += (self.direction*self.speed*self.speed*self.speed*self.speed)
		self.counter1 +=1
		
		if self.counter >= EXPLOSION_SPEED:
			self.counter = 0
			self.frame_index += 1
			if self.frame_index >= len(self.images):
				self.frame_index = 0
				if self.counter1 == 12:
					# self.frame_index = 0
					self.kill()
			else:
				self.image = self.images[self.frame_index]

########################################################
bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
aAttack_group = pygame.sprite.Group()
########################################################
sprite1 = Spritesheet("img/trainer_sheet.png")	# walk
sprite2 = Spritesheet("img/Idle.png")		# idle
sprite3 = Spritesheet("img/Jump.png")		# jump
sprite4 = Spritesheet("img/Attack.png")		# attack
sprite5 = Spritesheet("img/AttackCombo.png")	# attack combo


walk = []
idle = []
jump = []
attack = []

############### 0    1      2     3 ##################3
all_action = [idle, walk, jump, attack]
getImage(idle, sprite2, 1, 11, 'Idle', 1)
getImage(walk, sprite1, 1, 11, 'run', 1)
getImage(jump, sprite3, 1, 4, 'jump', 1)
getImage(attack, sprite5, 1, 11, 'AttackCombo', 1)

################# OBJECT CLASS ####################
player = Character(all_action, 200, 200, 3,100)
enemy = Character(all_action, 400, 200, 3,100)

health_bar = healthBar(30, 0, 100, 100)

enemy_group = pygame.sprite.Group()

enemy_group.add(enemy)

scroll = 0

run = True
while run:

	clock.tick(FPS)
	
	draw_bg()
	health_bar.draw(player.health)
	draw_text('Hp', font, RED, 0, 0)
	player.update()
	player.draw()
	for enemy in enemy_group:
		enemy.ai(3, 11)
		enemy.update()
		enemy.draw()

	aAttack_group.update()
	aAttack_group.draw(screen)
	bullet_group.update()
	bullet_group.draw(screen)
	explosion_group.update()
	explosion_group.draw(screen)
	############## if ACTION ################
	if player.alive:
		if shoot:
			player.update_action(3)
		elif player.attack:
			# player.frame_attacks(3, 11)
			n = 0
			while n < 10:
				n+=1
				player.attacker()
		elif move_left or move_right:
			player.update_action(1)	# walk
			if player.rect.bottom != 610:
				player.update_action(2)
		elif player.in_air:
			player.update_action(2)	# jump
		else:
			player.update_action(0)	# idle
		
	player.move(move_left, move_right)
	
	###################KEYBOARD INPUT########################
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				run = False
			if event.key == pygame.K_LEFT:
				move_left = True
			if event.key == pygame.K_RIGHT:
				move_right = True
			if event.key == pygame.K_UP and player.alive:
				player.jump = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_1:
				player.attack = True
				

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				move_left = False
			if event.key == pygame.K_RIGHT:
				move_right = False
			if event.key == pygame.K_SPACE:
				shoot = False
			if event.key == pygame.K_1:
				player.attack = False

	pygame.display.update()
pygame.quit()
