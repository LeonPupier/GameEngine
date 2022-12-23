import pygame, glob
from random import randint

from interaction import *

class World_Effect():
	def __init__(self, screen, size, save_world):
		self.screen = screen
		self.size = size

		self.effect = save_world[7]
		self.list_particules = []
		self.list_particules_ground = []
		self.list_time_particules_ground = []

		# Name and size of particule
		with open('Content/Textures/Effects/particules.dll') as list_effect:
			self.list_content_effect = list_effect.read().splitlines()

		# Name of effect
		self.list_support_effect = []
		for element in self.list_content_effect:
			info_effect = element.split('.')
			name_effect = info_effect[0]

			if name_effect == self.effect:
				self.size_particule_multiplier = int(info_effect[1])

			self.list_support_effect.append(name_effect)

		self.class_interaction = Interaction(screen, size)

		self.fps_particules = 0
		self.fps_flash_particule = 0
		self.time_flash_particule = 0
		self.blit_flash_particule = False
		self.time_blit_flash_particule = 0

		try:
			self.class_interaction.play_sound(f'{self.effect}_outside', nb_play=-1)
		except FileNotFoundError:
			pass

		if self.effect != 'None':
			self.images_effect = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Effects/' + self.effect + '/*.png')]

			# Size particule
			self.size_particule = self.images_effect[0].get_size()
			self.real_size_particule = self.size_particule[0] * self.size_particule_multiplier

			self.resize_effect = (int((self.size[0]*self.real_size_particule)/1920), int((self.size[1]*self.real_size_particule)/1080))
			self.images_effect = [pygame.transform.scale(self.image, self.resize_effect) for self.image in self.images_effect]

			if self.effect in self.list_support_effect:
				self.image_filter = pygame.image.load(f'Content/Textures/Effects/{self.effect}_filter.png').convert_alpha()
				self.image_filter = pygame.transform.scale(self.image_filter, self.size)

				self.image_flash = pygame.image.load(f'Content/Textures/Effects/{self.effect}_flash.png').convert_alpha()
				self.image_flash = pygame.transform.scale(self.image_flash, self.size)

			self.spawn_out_screen = self.resize_effect[0]
			self.speed_effect = int((self.size[0]*20)/1920)

			# Speed particule
			if self.effect == 'rain':
				self.time_particules = 1

			elif self.effect == 'flake':
				self.time_particules = 5

	def show_ground_effect(self, x, y):
		if self.effect in self.list_support_effect:
			for particule in self.list_particules_ground:
				new_position = (particule[0]+x, particule[1]+y)
				index_particule = self.list_particules_ground.index(particule)

				if self.list_time_particules_ground[index_particule] != 120:
					self.list_particules_ground[index_particule] = new_position
					self.list_time_particules_ground[index_particule] += 1

					self.screen.blit(self.images_effect[-1], new_position)

				else:
					self.list_particules_ground.remove(particule)
					del self.list_time_particules_ground[index_particule]

	def show(self):
		if self.effect != 'None':
			if self.fps_particules == self.time_particules:
				if randint(1,2) == 1:
					random_position = (randint(-self.spawn_out_screen, 0), randint(-self.spawn_out_screen, self.size[1])) # Axe vertical
				else:
					random_position = (randint(0, self.size[0]), randint(-self.spawn_out_screen, 0)) # Axe horizontal

				self.list_particules.append(random_position)
				self.fps_particules = 0

			else:
				self.fps_particules += 1

			# Add ground particule
			for particule in self.list_particules:
				if particule[0] <= self.size[0] and particule[1] <= self.size[1]:
					self.idx_effect = 0

					if randint(1,100) == 100 and self.effect in self.list_support_effect:
						self.screen.blit(self.images_effect[-1], particule)
						self.list_particules_ground.append(particule)
						self.list_time_particules_ground.append(0)
						self.list_particules.remove(particule)
					else:
						self.screen.blit(self.images_effect[self.idx_effect], particule)

						new_position_particule = (particule[0]+self.speed_effect, particule[1]+self.speed_effect)
						self.list_particules[self.list_particules.index(particule)] = new_position_particule

				else:
					self.list_particules.remove(particule)

			if self.effect in self.list_support_effect:
				self.screen.blit(self.image_filter, (0,0))

			if self.fps_flash_particule == 0:
				self.time_flash_particule = randint(5, 60)*60
				self.fps_flash_particule += 1

			elif self.fps_flash_particule == self.time_flash_particule:
				self.class_interaction.play_sound('lightning_bolt')
				self.fps_flash_particule = 0

				if self.effect in self.list_support_effect:
					self.blit_flash_particule = True

			else:
				self.fps_flash_particule += 1

			if self.blit_flash_particule == True:
				if self.time_blit_flash_particule != 15:
					self.screen.blit(self.image_flash, (0,0))
					self.time_blit_flash_particule += 1
				else:
					self.time_blit_flash_particule = 0
					self.blit_flash_particule = False

######################################################################################################################################################

class Effect():
	def __init__(self, screen, size, name_effect, position, size_mesh):
		self.screen = screen
		self.size = size
		self.size_mesh = size_mesh

		self.images_effect = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Effects/' + name_effect + '/*.png')]

		self.size_particule = self.images_effect[0].get_size()[0]*2
		self.resize_effect = (int((self.size[0]*self.size_particule)/1920), int((self.size[1]*self.size_particule)/1080))

		self.images_effect = [pygame.transform.scale(self.image, self.resize_effect) for self.image in self.images_effect]

		self.list_particules = []
		self.fps_particules = 0
		self.idx_effect = 1
		self.speed_effect = int((self.size[0]*8)/1920)

	def show(self, xy):
		if self.fps_particules == 0:
			x = randint(int(xy[0]), int(xy[0]+self.size_mesh[0]))
			position_particule = (x, xy[1])
			self.list_particules.append(position_particule)

		elif self.fps_particules == 30:
			self.fps_particules = 0

		if self.idx_effect in (0, 1):
			self.idx_effect += 1
		elif self.idx_effect == 2:
			self.idx_effect -= 1

		for particule in self.list_particules:
			new_position_particule = (particule[0], particule[1]+self.speed_effect)
			self.list_particules[self.list_particules.index(particule)] = new_position_particule

			self.screen.blit(self.images_effect[self.idx_effect], new_position_particule)

		self.fps_particules += 1