import pygame, glob, os

from interaction import *

class Building():
	def __init__(self, id_mesh, screen, size, name_building, language_interaction, position):
		self.id = id_mesh
		self.screen = screen
		self.size = size
		self.name_building = name_building

		self.images = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Buildings/' + self.name_building + '/*.png')]

		self.size_default = self.images[0].get_size()
		self.resize = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))

		self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]

		self.idx = 0
		self.wait_action = False
		self.rect = self.images[0].get_rect()
		self.xy = position
		self.rect = self.rect.move(self.xy)
		self.interaction_class = Interaction(self.screen, self.size)

		self.txt_interact_toquer = language_interaction[12]
		self.txt_interact_rentrer = language_interaction[13]
		self.txt_interact_fermer = language_interaction[14]
		self.current_text_interact = self.txt_interact_toquer

	def waiting_user_action(self, Keys, Joystick_Keys):
		if Keys[pygame.K_e] or Joystick_Keys.get_button(0):
			if not self.wait_action:

				# Change house's texture
				if self.idx == 0:
					self.current_text_interact = self.txt_interact_fermer
					self.interaction_class.play_sound('open_door')
					self.idx = 1
				else:
					self.current_text_interact = self.txt_interact_toquer
					self.interaction_class.play_sound('close_door')
					self.idx = 0

				self.wait_action = True
		else:
			self.wait_action = False
			return ('e', self.current_text_interact)

	def show(self, x=0, y=0):
		self.old_position = self.xy
		self.xy = (self.xy[0]+x, self.xy[1]+y)
		self.rect.x, self.rect.y = self.xy[0], self.xy[1]

		if self.name_building == '10': # House
			self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/4, self.resize[0], self.resize[1]/5.5))

		elif self.name_building == '11': # Manor
			self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/3, self.resize[0], self.resize[1]/3))

		self.screen.blit(self.images[self.idx], self.xy)