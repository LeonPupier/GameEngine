import pygame, pickle

from objects import *
from environment import *
from pnj import *
from building import *

from interaction import *
from ui import Entry

def current_map_save(map_index):
	file_map = open('Content/Maps/current_map.dll', 'w')
	file_map.write(str(map_index))
	file_map.close()

class MapMainMenu():
	def __init__(self):
		# Initialisation display
		self.group_blit = []
		self.group_collision = []
		self.group_light = []
		self.liste_interact = []
		self.liste_movement = []

		self.list_collision_border = []
		self.list_collision_id = []

class Map():
	def __init__(self, screen, size, name_map, sound, size_tile, save_class, player, editor):
		self.screen = screen
		self.size_tile = size_tile
		self.sound = sound
		self.name_map = str(name_map)
		self.player = player
		self.editor = editor
		
		path_save = save_class.path()
		language = save_class.current_language()
		language_interaction = save_class.load_language('interaction')

		save_player = save_class.list_save[0]
		save_world = save_class.list_save[1]
		save_quests = save_class.list_save[2]
		save_id_dialog = save_class.list_save[3]
		save_inventory = save_class.list_save[4]

		# Position map
		self.xy = (0,0)

		# Player position for tile sound
		resize_player = (int((size[0]*96)/1920), int((size[1]*132)/1080))
		self.x_player = size[0]/2
		self.y_player = size[1]/2+resize_player[1]/2
		self.fps_footstep = 0

		# Display initialisation
		self.group_blit = []
		self.group_collision = []
		self.group_light = []
		self.liste_interact = []
		self.liste_movement = []

		self.list_collision_border = []
		self.list_border_xy = []
		self.list_collision_id = []

		# Pre init
		self.group_blit.append(self.player)
		self.sound.play_sound(self.name_map, nb_play=10000000)

		# Ground generation
		try:
			with open('Content/Maps/' + self.name_map + '/ground.plk', 'rb') as data_ground:
					self.list_tiles = pickle.load(data_ground)
		except:
			self.list_tiles = []

		self.tiles_map = []

		for index_level, level in enumerate(self.list_tiles):
			self.tiles_map.append([])
			for tile in level:
				image_tile = pygame.image.load(f'Content/Textures/Tiles/{str(tile[0]+10)}.png').convert_alpha()
				image_tile = pygame.transform.scale(image_tile, (self.size_tile, self.size_tile))
				image_tile = pygame.transform.flip(image_tile, tile[3], False)
				image_tile = pygame.transform.rotate(image_tile, tile[2])
				self.tiles_map[index_level].append([image_tile, tile[1]])

		# Meshs generation
		try:
			with open('Content/Maps/' + self.name_map + '/landscape.maps') as list_mesh_map:
				mesh_map = list_mesh_map.read().splitlines()
		except FileNotFoundError:
			print("File map not found in the define folder...")
			return

		mesh_id = 0
		for mesh in mesh_map:
			# Init blit mesh
			try:
				mesh_instance = mesh.split(' | ')

				name_fonction = mesh_instance[0]
				mesh_attribute = mesh_instance[1].split(', ')

				mesh_position = mesh_attribute[-1].split(';')
				mesh_position = (size_tile*int(mesh_position[0]), size_tile*int(mesh_position[1]))
			except:
				# Collisions map
				try:
					collision_rect = mesh.split(' ')
					mode_rect = collision_rect[0]
					name_rect = collision_rect[2]
					collision_rect = collision_rect[1]
					collision_rect = collision_rect.split('|')

					start_collision = collision_rect[0].split(';')
					end_collision = collision_rect[1].split(';')

					if mode_rect == 'classic':
						size_rect = 96

					elif mode_rect == 'slim':
						size_rect = 16

					x_start = int(start_collision[0])*size[0]*96/1920
					y_start = int(start_collision[1])*size[0]*96/1920
					x_end = int(end_collision[0])*size[0]*size_rect/1920
					y_end = int(end_collision[1])*size[0]*size_rect/1920

					rect_collision = pygame.Rect(x_start, y_start, x_end, y_end)
					self.list_collision_border.append(rect_collision)
					self.list_border_xy.append((rect_collision.x, rect_collision.y))
					self.list_collision_id.append(name_rect)

				except (IndexError, ValueError):
					name_fonction = None

			mesh_id += 1

			# Objects
			try:
				if name_fonction == 'Post':
					mesh_add = Post(mesh_id, screen, size, mesh_attribute[0], mesh_position)
					self.group_blit.append(mesh_add)
					self.group_collision.append(mesh_add)

				elif name_fonction == 'Portal':
					mesh_add = Portal(mesh_id, screen, size, mesh_attribute[0], language_interaction, mesh_position)
					self.group_blit.append(mesh_add)
					self.group_collision.append(mesh_add)
					self.liste_interact.append(mesh_add)

				elif name_fonction == 'Banner':
					mesh_add = Banner(mesh_id, screen, size, mesh_attribute[0], mesh_position)
					self.group_blit.append(mesh_add)
					self.group_collision.append(mesh_add)

				elif name_fonction == 'Chest':
					mesh_add = Chest(mesh_id, screen, size, mesh_attribute[0], language_interaction, mesh_position, save_class)
					self.group_blit.append(mesh_add)
					self.group_collision.append(mesh_add)
					self.liste_interact.append(mesh_add)

				elif name_fonction == 'Pot':
					mesh_add = Pot(mesh_id, screen, size, mesh_attribute[0], language_interaction, mesh_position)
					self.group_blit.append(mesh_add)
					self.group_collision.append(mesh_add)
					self.liste_interact.append(mesh_add)

				# Environment
				elif name_fonction == 'Grass':
					mesh_add = Grass(mesh_id, screen, size, mesh_attribute[0], bool(mesh_attribute[1]), mesh_position)
					self.group_blit.append(mesh_add)

				elif name_fonction == 'Flower':
					mesh_add = Flower(mesh_id, screen, size, mesh_attribute[0], mesh_position)
					self.group_blit.append(mesh_add)

				elif name_fonction == 'Tree':
					mesh_add = Tree(mesh_id, screen, size, mesh_attribute[0], language_interaction, mesh_position)
					self.group_blit.append(mesh_add)
					self.group_collision.append(mesh_add)
					self.liste_interact.append(mesh_add)

				elif name_fonction == 'Bush':
					mesh_add = Bush(mesh_id, screen, size, mesh_attribute[0], mesh_position)
					self.group_blit.append(mesh_add)

				# Building
				elif name_fonction == 'Building':
					mesh_add = Building(mesh_id, screen, size, mesh_attribute[0], language_interaction, mesh_position)
					self.group_blit.append(mesh_add)
					self.group_collision.append(mesh_add)
					self.liste_interact.append(mesh_add)

				# Entity
				elif name_fonction == 'Pnj':
					mesh_add = Pnj(mesh_id, screen, size, language, int(mesh_attribute[0]), mesh_position, language_interaction, path_save, save_player, save_id_dialog)
					self.group_blit.append(mesh_add)
					self.group_collision.append(mesh_add)
					self.liste_interact.append(mesh_add)
					self.liste_movement.append(mesh_add)

			except Exception as error:
				print(f"An error occured during the mesh loading for '{name_fonction}' : {error}.")

	def show(self, Keys, x=0, y=0):
		dt = float(os.environ['DELTA_TIME'])

		if self.editor == False:
			self.xy = (self.xy[0]+x, self.xy[1]+y)

			# Borders
			for idx_border, border in enumerate(self.list_collision_border):
				border.x, border.y = self.list_border_xy[idx_border][0]+self.xy[0], self.list_border_xy[idx_border][1]+self.xy[1]

			# Display tile
			for index_level, level in enumerate(self.tiles_map):
				for index_tile, tile in enumerate(level):
					xy_tile = (tile[1][0]*self.size_tile+self.xy[0], tile[1][1]*self.size_tile+self.xy[1])

					self.screen.blit(tile[0], xy_tile)

					if Keys[pygame.K_F10]:
						pygame.draw.line(self.screen, 'grey', xy_tile, (xy_tile[0]+self.size_tile, xy_tile[1]))
						pygame.draw.line(self.screen, 'grey', xy_tile, (xy_tile[0], xy_tile[1]+self.size_tile))

					# Find tile id for walk sound
					if index_level == 0:
						collision_x = tile[1][0]*self.size_tile+self.xy[0] < self.x_player < tile[1][0]*self.size_tile+self.size_tile+self.xy[0]
						collision_y = tile[1][1]*self.size_tile+self.xy[1] < self.y_player < tile[1][1]*self.size_tile+self.size_tile+self.xy[1]

						if collision_x and collision_y:
							id_collision_tile = self.list_tiles[0][index_tile][0]+10
							sound_walk = None

							# Grass
							if id_collision_tile in (22, 50):
								sound_walk = 'grass'

							# Ground
							elif id_collision_tile in (14, 32, 42):
								sound_walk = 'ground'

							# Rock
							elif id_collision_tile == 12:
								sound_walk = 'rock'

							# Sand
							elif id_collision_tile == 10:
								sound_walk = 'sand'

							# Play sound
							if x != 0 or y != 0:
								if sound_walk != None:
									if self.fps_footstep >= 0.4:
										self.sound.play_sound(sound_walk)
										self.fps_footstep = 0
									else:
										self.fps_footstep += dt
								else:
									self.fps_footstep = 0

'''
MAPS ID

main_menu: Main menu design
0: Test game engine

'''