import pygame, glob, os

from interaction import *

class Chest():
	def __init__(self, id_mesh, screen, size, name_chest, language_interaction, position, save_class):
		self.id = id_mesh
		self.save_class = save_class
		self.size = size

		self.images = []
		self.images.append(pygame.image.load('Content/Textures/Objects/chest/' + name_chest + '/10.png').convert_alpha())
		self.images.append(pygame.image.load('Content/Textures/Objects/chest/' + name_chest + '/10_open.png').convert_alpha())
		self.size_default = self.images[0].get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]

		self.idx = 0
		self.fps_count = 0
		self.time_count_item = 0
		self.time_animation = 0
		self.time_animation_item = 1
		self.screen = screen
		self.rect = self.images[0].get_rect()
		self.xy = position
		self.rect = self.rect.move(self.xy)
		self.interaction_class = Interaction(self.screen, self.size)

		self.size_font = int((self.size[0]*25)/1600)
		self.font = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font)
		self.angle = 0
		self.nb_gift = 0

		self.txt_interact = language_interaction[0]

	def interaction(self):
		dt = float(os.environ['DELTA_TIME'])

		# Contenu du coffre
		list_gift = [['gold_coin', 12]] #random_gift()

		if self.time_count_item <= self.time_animation_item:
			image_item = pygame.image.load('Content/Textures/Items/' + list_gift[self.nb_gift][0] + '.png').convert_alpha()
			resize_item = (int((self.size[0]*48)/1920), int((self.size[1]*48)/1080))
			image_item = pygame.transform.scale(image_item, resize_item)
			
			image_light = pygame.image.load('Content/Textures/Environment/light.png').convert_alpha()
			resize_light = (int((self.size[0]*100)/1600), int((self.size[1]*100)/900))
			image_light = pygame.transform.scale(image_light, resize_light)
			self.angle += 8
			rotate_light = pygame.transform.rotate(image_light, self.angle)
			rect_light = rotate_light.get_rect(center=image_light.get_rect(center=(self.xy[0]+resize_item[0], self.xy[1]-resize_item[1])).center)
			self.screen.blit(rotate_light, rect_light.topleft)

			nb_gift_txt = self.font.render(str(list_gift[self.nb_gift][1]), 1, 'black')
			xy_text_gift = (self.xy[0]+resize_item[0]/2, self.xy[1]-resize_item[1]*1.5)


			self.screen.blit(image_item, xy_text_gift)
			self.screen.blit(nb_gift_txt, xy_text_gift)

			self.time_count_item += dt
		else:
			self.interaction_class.play_sound('chest_gift')
			if self.nb_gift < len(list_gift)-1:
				self.nb_gift += 1
				self.angle = 0
				return 0, 0
			else:
				# Add rewards for the player
				for reward in list_gift:
					if reward[0] == 'gold_coin':
						self.save_class.transaction_money('+', reward[1])
				
				return 'delete'

	def waiting_user_action(self, Keys, Joystick_Keys):
		if Keys[pygame.K_e] or Joystick_Keys.get_button(0):
			self.interaction_class.play_sound('unlock')

			if self.fps_count >= self.time_animation:
				if self.idx < len(self.images)-1:
					self.idx += 1
				else:
					self.idx = 0
				self.fps_count = 0
			else:
				self.fps_count += dt

			return 'interaction'
		else:
			return ('e', self.txt_interact)

	def show(self, x=0, y=0):
		self.old_position = self.xy
		self.xy = (self.xy[0]+x, self.xy[1]+y)

		self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/3.5, self.resize[0], self.resize[1]/3.5))

		self.screen.blit(self.images[self.idx], self.xy)

######################################################################################################################################################

class Post():
	def __init__(self, id_mesh, screen, size, image, position):
		self.id = id_mesh
		self.size = size
		self.screen = screen

		self.images = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Objects/post/*.png')]
		self.size_default = self.images[0].get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]

		self.idx = int(image)-10
		self.rect = self.images[0].get_rect()
		self.xy = position

	def show(self, x=0, y=0):
		self.old_position = self.xy
		self.xy = (self.xy[0]+x, self.xy[1]+y)

		self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/3.5, self.resize[0], self.resize[1]/3.5))

		self.screen.blit(self.images[self.idx], self.xy)

######################################################################################################################################################

class Banner():
	def __init__(self, id_mesh, screen, size, name_banner, position):
		self.id = id_mesh
		self.size = size

		self.images = []

		self.images.append(pygame.image.load('Content/Textures/Objects/banner/' + name_banner + '.png').convert_alpha())

		self.size_default = self.images[0].get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]

		self.idx = 0
		self.screen = screen
		self.rect = self.image.get_rect()
		self.xy = position

	def show(self, x=0, y=0):
		self.old_position = self.xy
		self.xy = (self.xy[0]+x, self.xy[1]+y)

		self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/7, self.resize[0], self.resize[1]/7))

		self.screen.blit(self.images[self.idx], self.xy)

######################################################################################################################################################

class Pot():
	def __init__(self, id_mesh, screen, size, name_pot, language_interaction, position):
		self.id = id_mesh
		self.size = size

		self.images = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Objects/pot/' + name_pot + '/*.png')]
		self.size_default = self.images[0].get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]

		self.wait_action = False
		self.idx = 0
		self.fps_count = 0.08
		self.time_animation = 0.1
		self.screen = screen
		self.rect = self.image.get_rect()
		self.xy = (position[0], position[1])

		self.interaction_class = Interaction(self.screen, self.size)
		self.txt_interact = language_interaction[15]

	def waiting_user_action(self, Keys, Joystick_Keys):
		if Keys[pygame.K_e] or Joystick_Keys.get_button(0):
			self.interaction_class.play_sound('pot_break')
			return 'interaction'
		else:
			return ('e', self.txt_interact)

	def interaction(self):
		dt = float(os.environ['DELTA_TIME'])

		if self.idx != len(self.images)-1:
			if self.fps_count >= self.time_animation:
				if self.idx < len(self.images)-1:
					self.idx += 1
				else:
					self.idx = 0
				self.fps_count = 0
			else:
				self.fps_count += dt

		else:
			return 'delete'

	def show(self, x=0, y=0):
		self.old_position = self.xy
		self.xy = (self.xy[0]+x, self.xy[1]+y)

		self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/2, self.resize[0], self.resize[1]/2))
		self.screen.blit(self.images[self.idx], self.xy)

######################################################################################################################################################

class Portal():
	def __init__(self, id_mesh, screen, size, name_portal, language_interaction, position):
		self.id = id_mesh
		self.size = size

		self.images = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Objects/portal/' + name_portal + '/*.png')]
		self.size_default = self.images[0].get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]

		self.wait_action = False
		self.idx = 0
		self.screen = screen
		self.rect = self.image.get_rect()
		self.xy = position
		self.rect_interact = self.image.get_rect()

		self.interaction_class = Interaction(self.screen, self.size)
		self.txt_interact_open = language_interaction[0]
		self.txt_interact_close = language_interaction[14]

	def waiting_user_action(self, Keys, Joystick_Keys):
		if Keys[pygame.K_e] or Joystick_Keys.get_button(0):
			if self.wait_action == False:

				if self.idx == 0:
					self.idx = 1

				else:
					self.idx = 0

				self.wait_action = True
		
		else:
			self.wait_action = False
			if self.idx == 0:
				return ('e', self.txt_interact_open)
			return ('e', self.txt_interact_close)

	def show(self, x=0, y=0):
		self.old_position = self.xy
		self.xy = (self.xy[0]+x, self.xy[1]+y)

		self.rect_interact.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/3.5, self.resize[0], self.resize[1]/3.5))

		# Collision rect
		if self.idx == 0:
			self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/3.5, self.resize[0], self.resize[1]/3.5))
		else:
			self.rect.update((0, 0, 0, 0))

		self.screen.blit(self.images[self.idx], self.xy)