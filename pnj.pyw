import pygame, glob, os

from interaction import *

class Pnj():
	def __init__(self, id_mesh, screen, size, lang, id_pnj, position, language_interaction, path_save, save_player, save_id_dialog):
		self.id = id_mesh
		self.id_pnj = str(id_pnj)
		self.position = position
		
		self.images = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/' + self.id_pnj + '/*.png')]
		self.resize = (int((size[0]*96)/1920), int((size[1]*132)/1080))
		self.images = [pygame.transform.scale(self.image, self.resize) for self.image in self.images]

		# ID dialogue 
		self.id_dialog = int(save_id_dialog[id_pnj])

		# Max dialogue réplique
		with open('Content/Npc/max_dialog.dll', encoding='utf-8') as sentence:
			self.max_dialog = sentence.read().splitlines()
		self.max_dialog = int(self.max_dialog[id_pnj])

		# Liste phrases/répliques du pnj
		with open('Content/Languages/' + lang + '/' + self.id_pnj + '.dll', encoding='utf-8') as sentence:
			self.list_dialog = sentence.read().splitlines()

		# Pnj en mouvement
		with open('Content/Npc/movement.dll', encoding='utf-8') as sentence:
			self.movement = sentence.read().splitlines()
		self.movement = int(self.movement[id_pnj])

		self.time_walk = 0.15
		self.ms_walk = 0
		self.direction = 'down'
		self.movement = False
		self.idx = 0
		self.screen = screen
		self.rect = self.images[0].get_rect()
		self.xy = (position[0], position[1] - self.rect[0] + size[0]*64/1920)
		self.rect = self.rect.move(self.xy)

		self.txt_interact_main = language_interaction[6]
		
		self.side_action = save_player[9]

		if self.side_action == 'steal':
			self.txt_interact_ctrl = language_interaction[7]

		self.interaction_class = Interaction(screen, size)

	def waiting_user_action(self, Keys, Joystick_Keys):
		# KEYBOARD
		# Display speak
		if not Keys[convert_pygame_key(os.environ['KEYBOARD_ACTION'])] and not Keys[pygame.K_LCTRL]:
			return os.environ['KEYBOARD_ACTION'], self.txt_interact_main

		# Speak
		elif Keys[convert_pygame_key(os.environ['KEYBOARD_ACTION'])] and not Keys[pygame.K_LCTRL]:
			return 'interaction_dontremove'

		# Display secondary action
		elif not Keys[convert_pygame_key(os.environ['KEYBOARD_SIDE_ACTION'])] and Keys[pygame.K_LCTRL]:
			return os.environ['KEYBOARD_SIDE_ACTION'], self.txt_interact_ctrl

		# Secondary action
		elif Keys[convert_pygame_key(os.environ['KEYBOARD_SIDE_ACTION'])] and Keys[pygame.K_LCTRL]:
			# Secondary action system
			pass

		# CONTROLLER
		# ...

	def interaction(self):
		# Vérification du type de variable pour les dialogues maxs
		if int(self.id_dialog) == self.id_dialog:
			type_id_dialog = True # Integer avec 0
		else:
			type_id_dialog = False # Float avec 0.5

		# Dialog
		if self.id_dialog < self.max_dialog and type_id_dialog:
			self.id_dialog = self.interaction_class.dialog(self.list_dialog[int(self.id_dialog)], self.id_dialog)
		elif self.id_dialog >= self.max_dialog and type_id_dialog:
			self.id_dialog = self.interaction_class.dialog(self.list_dialog[-1], self.id_dialog)
		else:
			self.id_dialog += 0.5
			return 'delete'

		return 'disable_move' # Continue playing dialogue 'animation'

	def focus_point(self, xy_point, maps, object_collision=False):
		# Delta time correction
		dt = float(os.environ['DELTA_TIME'])
		self.pnj_speed = 225*dt
		self.pnj_speed_diagonal = 135*dt

		# Definition
		xy_backup = self.xy

		move_left = self.xy[0] > xy_point[0]+self.resize[0]
		move_right = self.xy[0] < xy_point[0]-self.resize[0]
		move_up = self.xy[1] > xy_point[1]+self.resize[1]/2
		move_down = self.xy[1] < xy_point[1]-self.resize[1]/2

		# Diagonals
		if move_left and move_up:
			self.xy = (self.xy[0]-self.pnj_speed_diagonal, self.xy[1]-self.pnj_speed_diagonal)
			if self.idx not in (3,4,5):
				self.idx = 3
			self.direction = 'left'
			self.movement = True

		elif move_left and move_down:
			self.xy = (self.xy[0]-self.pnj_speed_diagonal, self.xy[1]+self.pnj_speed_diagonal)
			if self.idx not in (3,4,5):
				self.idx = 3
			self.direction = 'left'
			self.movement = True

		elif move_right and move_up:
			self.xy = (self.xy[0]+self.pnj_speed_diagonal, self.xy[1]-self.pnj_speed_diagonal)
			if self.idx not in (6,7,8):
				self.idx = 6
			self.direction = 'right'
			self.movement = True

		elif move_right and move_down:
			self.xy = (self.xy[0]+self.pnj_speed_diagonal, self.xy[1]+self.pnj_speed_diagonal)
			if self.idx not in (6,7,8):
				self.idx = 6
			self.direction = 'right'
			self.movement = True

		# Axe x
		elif move_left:
			self.xy = (self.xy[0]-self.pnj_speed, self.xy[1])
			if self.idx not in (3,4,5):
				self.idx = 3
			self.direction = 'left'
			self.movement = True

		elif move_right:
			self.xy = (self.xy[0]+self.pnj_speed, self.xy[1])
			if self.idx not in (6,7,8):
				self.idx = 6
			self.direction = 'right'
			self.movement = True

		# Axe y
		elif move_up:
			self.xy = (self.xy[0], self.xy[1]-self.pnj_speed)
			if self.idx not in (9,10,11):
				self.idx = 9
			self.direction = 'up'
			self.movement = True

		elif move_down:
			self.xy = (self.xy[0], self.xy[1]+self.pnj_speed)
			if self.idx not in (0,1,2):
				self.idx = 0
			self.direction = 'down'
			self.movement = True

		# End of the traject
		else:
			self.movement = False

		# Return to position before collision
		self.rect.x, self.rect.y = self.xy[0], self.xy[1]
		self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/3.5, self.resize[0], self.resize[1]/3.5))

		for objects in maps.group_collision:
			if self.rect.colliderect(objects.rect) and self.rect != objects.rect:
				self.xy = xy_backup
				self.movement = False
				break

		for borders in maps.list_collision_border:
			if self.rect.colliderect(borders):
				self.xy = xy_backup
				self.movement = False
				break

		self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/3.5, self.resize[0], self.resize[1]/3.5))

		# Walking animation
		if self.ms_walk >= self.time_walk:
			if self.direction == 'down':
				if self.idx < 2:
					self.idx += 1
				else:
					self.idx = 0

			elif self.direction == 'up':
				if self.idx < 11:
					self.idx += 1
				else:
					self.idx = 9

			elif self.direction == 'left':
				if self.idx < 5:
					self.idx += 1
				else:
					self.idx = 3

			elif self.direction == 'right':
				if self.idx < 8:
					self.idx += 1
				else:
					self.idx = 6

			self.ms_walk = 0

		else:
			self.ms_walk += dt

		# No movement
		if self.movement == False:
			if self.direction == 'down':
				self.idx = 0

			elif self.direction == 'up':
				self.idx = 9

			elif self.direction == 'left':
				self.idx = 3

			elif self.direction == 'right':
				self.idx = 6

	def show(self, x=0, y=0):
		self.old_position = self.xy
		self.xy = (self.xy[0]+x, self.xy[1]+y)

		self.rect.x, self.rect.y = self.xy[0], self.xy[1]
		self.rect.update((self.xy[0], self.xy[1]+self.resize[1]-self.resize[1]/3.5, self.resize[0], self.resize[1]/3.5))

		self.screen.blit(self.images[self.idx], self.xy)