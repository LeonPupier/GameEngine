import pygame, glob, os
from random import randint

from effects import Effect
from interaction import *

class Grass():
	def __init__(self, id_mesh, screen, size, name_grass, animate, position):
		self.id = id_mesh
		self.size = size
		
		if animate == True:
			self.images = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Environment/grass/' + name_grass + '/*.png')]
			self.size_default = self.images[0].get_size()
			self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
			self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]
		else:
			self.images = [pygame.image.load('Content/Textures/Environment/grass/' + name_grass + '.png').convert_alpha()]
			self.size_default = self.images.get_size()
			self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
			self.images = [pygame.transform.scale(self.images[0], self.resize)]

		self.idx = 0
		self.fps_count = 0
		self.time_animation = 1
		self.screen = screen
		self.rect = self.images[0].get_rect()
		self.xy = position
		self.rect = self.rect.move(self.xy)

	def show(self, x=0, y=0):
		dt = float(os.environ['DELTA_TIME'])

		self.xy, self.rect, self.rect.x, self.rect.y = move_map(self.screen, self.rect, x, y, self.xy)

		if self.fps_count >= self.time_animation:
			if self.idx < len(self.images)-1:
				self.idx += 1
			else:
				self.idx = 0
			self.fps_count = 0
		else:
			self.fps_count += dt

		self.screen.blit(self.images[self.idx], self.xy)

######################################################################################################################################################

class Flower():
	def __init__(self, id_mesh, screen, size, name_flower, position):
		self.id = id_mesh
		self.size = size
		
		self.images = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Environment/flower/' + name_flower + '/*.png')]
		self.size_default = self.images[0].get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]

		self.idx = 0
		self.fps_count = 0
		self.time_animation = 2
		self.screen = screen
		self.rect = self.images[0].get_rect()
		self.xy = position
		self.rect = self.rect.move(self.xy)

	def show(self, x=0, y=0):
		dt = float(os.environ['DELTA_TIME'])

		self.xy, self.rect, self.rect.x, self.rect.y = move_map(self.screen, self.rect, x, y, self.xy)
		
		if self.fps_count >= self.time_animation:
			if self.idx < len(self.images)-1:
				self.idx += 1
			else:
				self.idx = 0
			self.fps_count = 0
		else:
			self.fps_count += dt

		self.screen.blit(self.images[self.idx], self.xy)

######################################################################################################################################################

class Bush():
	def __init__(self, id_mesh, screen, size, name_bush, position):
		self.id = id_mesh
		self.screen = screen
		self.size = size

		self.image = pygame.image.load('Content/Textures/Environment/bush/' + name_bush + '.png').convert_alpha()
		self.size_default = self.image.get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.image = pygame.transform.scale(self.image, self.resize)

		self.image_hide_player = pygame.image.load('Content/Ui/hud/hide_player.png').convert_alpha()
		self.resize_hide_player = (int(size[0]), int(size[1]))
		self.image_hide_player = pygame.transform.scale(self.image_hide_player, self.resize_hide_player)

		self.blit_up_hud = False
		self.show_hide_focus = False
		self.opacity = 255
		self.opacity_hud = 0
		self.rect = self.image.get_rect()
		self.xy = position
		self.rect = self.rect.move(self.xy)

		self.blit_up_sound = True

	def blit_up_action(self):
		self.blit_up_hud = True
		self.show_hide_focus = True

		self.blit_up_sound = False

		if self.opacity > 140:
			self.opacity -= 5
			self.image.set_alpha(self.opacity)

	def blit_hud_action(self):
		if self.show_hide_focus == True:
			if self.opacity_hud < 140:
				self.opacity_hud += 2
				self.image_hide_player.set_alpha(self.opacity_hud)
			self.screen.blit(self.image_hide_player, (0, 0))

		else:
			if self.opacity_hud > 0:
				self.opacity_hud -= 2
				self.image_hide_player.set_alpha(self.opacity_hud)
				self.screen.blit(self.image_hide_player, (0, 0))

			if self.opacity_hud == 0:
				self.blit_up_hud = False

	def show(self, x=0, y=0):
		self.xy, self.rect, self.rect.x, self.rect.y = move_map(self.screen, self.rect, x, y, self.xy)
		self.screen.blit(self.image, self.xy)

######################################################################################################################################################

class Tree():
	def __init__(self, id_mesh, screen, size, name_tree, language, position):
		self.id = id_mesh
		self.size = size

		self.image = pygame.image.load('Content/Textures/Environment/tree/' + name_tree + '.png').convert_alpha()
		self.size_default = self.image.get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.image = pygame.transform.scale(self.image, self.resize)

		self.opacity = 255
		self.screen = screen
		self.rect = self.image.get_rect()
		self.xy = position
		self.xy_backup = position
		self.rect = self.rect.move(self.xy)
		self.time_count_animation = 0
		self.shake_placement = 0

		self.interaction_class = Interaction(self.screen, self.size)
		self.effect_class = Effect(screen, size, 'leaf', self.xy, self.resize)
		self.txt_interact = language[11]

	def blit_up_action(self):
		if self.opacity > 140:
				self.opacity -= 5
		self.image.set_alpha(self.opacity)

	def waiting_user_action(self, Keys, Joystick_Keys):
		if Keys[pygame.K_e] or Joystick_Keys.get_button(0):
			return 'interaction'
		else:
			self.interaction_class.waiting_key('e', self.txt_interact)

	def interaction(self):
		dt = float(os.environ['DELTA_TIME'])

		# Play sound design
		if self.time_count_animation == 0:
			self.interaction_class.play_sound('tree_shake')

		# Vibre sur les côtés
		if self.time_count_animation < 0.5:
			if self.shake_placement % 2 == 0:
				self.xy_backup = (self.xy[0], self.xy[1])
				self.xy = (self.xy[0]+10, self.xy[1])
			else:
				self.xy = (self.xy[0]-10, self.xy[1])
			self.shake_placement += 1

		else:
			self.xy = self.xy_backup
			return 'delete'

		self.time_count_animation += dt

	def show(self, x=0, y=0):
		self.xy = (self.xy[0]+x, self.xy[1]+y)

		# Particules leaf effect
		#self.effect_class.show(self.xy)

		self.rect.update((self.xy[0]+self.resize[0]/3, self.xy[1]+self.resize[1]-self.resize[1]/5, self.resize[0]/3, self.resize[1]/5))
		self.screen.blit(self.image, self.xy)