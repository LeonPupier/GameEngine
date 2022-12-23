import pygame, glob, os
from random import randint

class Player():
	def __init__(self, screen, size, save_player, editor=False):
		# Data
		self.id = 'Player'
		self.screen = screen
		self.size = size

		# Infos player
		self.name = save_player[0]
		self.sex = save_player[1]
		self.hairs = str(save_player[2])
		self.eye = str(save_player[3])
		self.body = str(save_player[4])
		self.leg = str(save_player[5])
		self.foot = str(save_player[6])
		self.skin = str(save_player[7])
		self.weapons = str(save_player[8])
		self.resize = (int((size[0]*96)/1920), int((size[1]*132)/1080))

		# Skin color
		self.images_up_skin = pygame.image.load('Content/Textures/Characters/player/skin/up/' + self.skin + '.png').convert_alpha()
		self.images_down_skin = pygame.image.load('Content/Textures/Characters/player/skin/down/' + self.skin + '.png').convert_alpha()
		self.images_left_skin = pygame.image.load('Content/Textures/Characters/player/skin/left/' + self.skin + '.png').convert_alpha()
		self.images_right_skin = pygame.image.load('Content/Textures/Characters/player/skin/right/' + self.skin + '.png').convert_alpha()
		self.images_up_skin = pygame.transform.scale(self.images_up_skin, self.resize)
		self.images_down_skin = pygame.transform.scale(self.images_down_skin, self.resize)
		self.images_left_skin = pygame.transform.scale(self.images_left_skin, self.resize)
		self.images_right_skin = pygame.transform.scale(self.images_right_skin, self.resize)

		# Hairs
		self.images_up_hairs = pygame.image.load('Content/Textures/Characters/player/hairs/up/' + self.hairs + '.png').convert_alpha()
		self.images_down_hairs = pygame.image.load('Content/Textures/Characters/player/hairs/down/' + self.hairs + '.png').convert_alpha()
		self.images_left_hairs = pygame.image.load('Content/Textures/Characters/player/hairs/left/' + self.hairs + '.png').convert_alpha()
		self.images_right_hairs = pygame.image.load('Content/Textures/Characters/player/hairs/right/' + self.hairs + '.png').convert_alpha()
		self.images_up_hairs = pygame.transform.scale(self.images_up_hairs, self.resize)
		self.images_down_hairs = pygame.transform.scale(self.images_down_hairs, self.resize)
		self.images_left_hairs = pygame.transform.scale(self.images_left_hairs, self.resize)
		self.images_right_hairs = pygame.transform.scale(self.images_right_hairs, self.resize)

		# Eye
		self.images_down_eye = pygame.image.load('Content/Textures/Characters/player/eye/down/' + self.eye + '.png').convert_alpha()
		self.images_left_eye = pygame.image.load('Content/Textures/Characters/player/eye/left/' + self.eye + '.png').convert_alpha()
		self.images_right_eye = pygame.image.load('Content/Textures/Characters/player/eye/right/' + self.eye + '.png').convert_alpha()
		self.images_down_eye = pygame.transform.scale(self.images_down_eye, self.resize)
		self.images_left_eye = pygame.transform.scale(self.images_left_eye, self.resize)
		self.images_right_eye = pygame.transform.scale(self.images_right_eye, self.resize)

		# Body
		self.images_up_body = pygame.image.load('Content/Textures/Characters/player/body/up/' + self.body + '.png').convert_alpha()
		self.images_down_body = pygame.image.load('Content/Textures/Characters/player/body/down/' + self.body + '.png').convert_alpha()
		self.images_left_body = pygame.image.load('Content/Textures/Characters/player/body/left/' + self.body + '.png').convert_alpha()
		self.images_right_body = pygame.image.load('Content/Textures/Characters/player/body/right/' + self.body + '.png').convert_alpha()
		self.images_up_body = pygame.transform.scale(self.images_up_body, self.resize)
		self.images_down_body = pygame.transform.scale(self.images_down_body, self.resize)
		self.images_left_body = pygame.transform.scale(self.images_left_body, self.resize)
		self.images_right_body = pygame.transform.scale(self.images_right_body, self.resize)

		# Leg
		self.images_up_leg = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/leg/up/' + self.leg + '/*.png')]
		self.images_down_leg = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/leg/down/' + self.leg + '/*.png')]
		self.images_left_leg = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/leg/left/' + self.leg + '/*.png')]
		self.images_right_leg = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/leg/right/' + self.leg + '/*.png')]
		self.images_up_leg = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_up_leg]
		self.images_down_leg = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_down_leg]
		self.images_left_leg = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_left_leg]
		self.images_right_leg = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_right_leg]

		# Foot
		self.images_up_foot = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/foot/up/' + self.foot + '/*.png')]
		self.images_down_foot = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/foot/down/' + self.foot + '/*.png')]
		self.images_left_foot = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/foot/left/' + self.foot + '/*.png')]
		self.images_right_foot = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/foot/right/' + self.foot + '/*.png')]
		self.images_up_foot = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_up_foot]
		self.images_down_foot = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_down_foot]
		self.images_left_foot = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_left_foot]
		self.images_right_foot = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_right_foot]

		# Weapons
		self.images_up_weapons = pygame.image.load('Content/Textures/Characters/player/weapons/up/' + self.weapons + '.png').convert_alpha()
		self.images_down_weapons = pygame.image.load('Content/Textures/Characters/player/weapons/down/' + self.weapons + '.png').convert_alpha()
		self.images_left_weapons = pygame.image.load('Content/Textures/Characters/player/weapons/left/' + self.weapons + '.png').convert_alpha()
		self.images_right_weapons = pygame.image.load('Content/Textures/Characters/player/weapons/right/' + self.weapons + '.png').convert_alpha()
		self.images_up_weapons = pygame.transform.scale(self.images_up_weapons, self.resize)
		self.images_down_weapons = pygame.transform.scale(self.images_down_weapons, self.resize)
		self.images_left_weapons = pygame.transform.scale(self.images_left_weapons, self.resize)
		self.images_right_weapons = pygame.transform.scale(self.images_right_weapons, self.resize)

		# Shadow
		self.images_shadow = pygame.image.load('Content/Textures/Characters/player/shadow.png').convert_alpha()
		self.images_shadow = pygame.transform.scale(self.images_shadow, self.resize)

		# Water
		self.images_up_water = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/water/up/*.png')]
		self.images_down_water = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/water/down/*.png')]
		self.images_left_water = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/water/left/*.png')]
		self.images_right_water = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/player/water/right/*.png')]
		self.images_up_water = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_up_water]
		self.images_down_water = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_down_water]
		self.images_left_water = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_left_water]
		self.images_right_water = [pygame.transform.scale(self.image, self.resize) for self.image in self.images_right_water]

		# Data
		self.editor = editor
		self.images_direction = 'up'
		self.direction = 'down'
		self.idx = 0
		self.time_animation = 0.15
		self.fps_count = 0
		self.water_effect = False
		self.fps_eye = 0
		self.clignement = False
		self.time_eye_open = 3.5
		self.time_eye_close = 0.5
		self.xy = (size[0]/2-self.resize[0]/2, size[1]/2-self.resize[1]/2)
		self.fake_xy = (0,0)

		# Stats
		self.speed = size[0]*300/1600
		self.speed_diagonal = size[0]*180/1600
		self.heart = 2
		self.heart_max = 2
		self.stamina = 20
		self.xp = 0
		self.xp_max = 10

		# Stats weapons
		self.idx_weapons = 0
		self.show_weapons = False

		# Rect collision direction
		self.size_rect = self.resize[1]/6
		self.rect_up = self.images_up_body.get_rect()
		self.rect_up.update((self.xy[0]+self.resize[0]/3.8, self.xy[1]+self.resize[1]-self.size_rect/0.53, self.resize[0]/2, size[0]*5/1600*2))

		self.rect_down = self.images_up_body.get_rect()
		self.rect_down.update((self.xy[0]+self.resize[0]/3.8, self.xy[1]+self.resize[1]-self.size_rect/3.5, self.resize[0]/2, size[0]*5/1600*2))

		self.rect_left = self.images_up_body.get_rect()
		self.rect_left.update((self.xy[0]+self.resize[0]/6.7, self.xy[1]+self.resize[1]-self.size_rect*1.3, size[0]*5/1600*2.3, self.size_rect))

		self.rect_right = self.images_up_body.get_rect()
		self.rect_right.update((self.xy[0]+self.resize[0]/1.35, self.xy[1]+self.resize[1]-self.size_rect*1.3, size[0]*5/1600*2.3, self.size_rect))

		# Interaction hitbox
		self.hitbox = self.images_up_body.get_rect()
		self.size_hitbox = self.resize[1]/3
		self.hitbox.update((self.xy[0], self.xy[1]+self.resize[1]/2.5, self.resize[0], self.size_hitbox*2.5))

		# Delete collision and interaction rects for camera movement
		if self.editor == True:
			self.rect_up.update(0,0,0,0)
			self.rect_down.update(0,0,0,0)
			self.rect_left.update(0,0,0,0)
			self.rect_right.update(0,0,0,0)
			self.hitbox.update(0,0,0,0)

	def show(self, Keys, direction=None):
		dt = float(os.environ['DELTA_TIME'])

		if self.fps_count >= self.time_animation:
			if self.idx < len(self.images_direction):
				self.idx += 1
			else:
				self.idx = 0
			self.fps_count = 0

		# Collision against an object therefore inability to move
		if direction in ('up_collision', 'down_collision', 'left_collision', 'right_collision'):
			self.idx = 1

		if direction != None:
			self.direction = direction

		# No movement key is pressed
		else:
			self.idx = 1

		# Blink
		self.fps_eye += dt
		if self.fps_eye >= self.time_eye_open and not self.clignement:
			self.clignement = True
			self.fps_eye = 0
		elif self.fps_eye >= self.time_eye_close and self.clignement:
			self.clignement = False
			self.fps_eye = 0

		# Show/Hide the weapon
		if Keys[pygame.K_UP]:
			self.show_weapons = True
		elif Keys[pygame.K_DOWN]:
			self.show_weapons = False

		if self.editor == False:
			if self.direction == 'up' or self.direction == 'up_collision':
				self.screen.blit(self.images_shadow, self.xy)
				self.screen.blit(self.images_up_skin, self.xy)

				if self.show_weapons == True:
					self.screen.blit(self.images_up_weapons, self.xy)

				self.screen.blit(self.images_up_hairs, self.xy)
				self.screen.blit(self.images_up_body, self.xy)
				self.screen.blit(self.images_up_leg[self.idx], self.xy)
				self.screen.blit(self.images_up_foot[self.idx], self.xy)

				if self.water_effect == True:
					self.screen.blit(self.images_up_water[self.idx], self.xy)

			elif self.direction == 'down' or self.direction == 'down_collision':
				self.screen.blit(self.images_shadow, self.xy)
				self.screen.blit(self.images_down_skin, self.xy)

				if self.clignement == False:
					self.screen.blit(self.images_down_eye, self.xy)

				self.screen.blit(self.images_down_hairs, self.xy)
				self.screen.blit(self.images_down_body, self.xy)
				self.screen.blit(self.images_down_leg[self.idx], self.xy)
				self.screen.blit(self.images_down_foot[self.idx], self.xy)

				if self.show_weapons == True:
					self.screen.blit(self.images_down_weapons, self.xy)

				if self.water_effect == True:
					self.screen.blit(self.images_down_water[self.idx], self.xy)

			elif self.direction == 'left' or self.direction == 'left_collision':
				self.screen.blit(self.images_shadow, self.xy)
				self.screen.blit(self.images_left_skin, self.xy)

				if self.clignement == False:
					self.screen.blit(self.images_left_eye, self.xy)

				self.screen.blit(self.images_left_hairs, self.xy)
				self.screen.blit(self.images_left_body, self.xy)
				self.screen.blit(self.images_left_leg[self.idx], self.xy)
				self.screen.blit(self.images_left_foot[self.idx], self.xy)

				if self.show_weapons == True:
					self.screen.blit(self.images_left_weapons, self.xy)

				if self.water_effect == True:
					self.screen.blit(self.images_left_water[self.idx], self.xy)

			elif self.direction == 'right' or self.direction == 'right_collision':
				self.screen.blit(self.images_shadow, self.xy)

				if self.show_weapons == True:
					self.screen.blit(self.images_right_weapons, self.xy)

				self.screen.blit(self.images_right_skin, self.xy)

				if self.clignement == False:
					self.screen.blit(self.images_right_eye, self.xy)

				self.screen.blit(self.images_right_hairs, self.xy)
				self.screen.blit(self.images_right_body, self.xy)
				self.screen.blit(self.images_right_leg[self.idx], self.xy)
				self.screen.blit(self.images_right_foot[self.idx], self.xy)

				if self.water_effect == True:
					self.screen.blit(self.images_right_water[self.idx], self.xy)

		self.fps_count += dt