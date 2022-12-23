import pygame, pickle, glob, time

# Map editor
class Editor():
	
	def __init__(self, screen, size, size_tile, name_map):
		self.screen = screen
		self.size = size
		self.name_map = name_map
		self.font = pygame.font.Font("Content/Fonts/pixel_game.ttf", int((size[0]*25)/1600))
		self.txt_map_saved = 'Map not saved'

		self.size_tile = size_tile
		self.list_new_mesh = []
		self.idx_mesh = 0
		self.idx_model = 0
		self.idx_tile = 0
		self.level_tile = 0
		self.remove_ground_mode = False
		self.xy = (0,0)
		self.xy_move_map = (0,0)
		self.angle_tile = 0
		self.flip_image = False
		self.mode = 'MESH'

		# Ground
		try:
			with open(f'Content/Maps/{self.name_map}/ground.plk', 'rb') as data_ground:
				self.list_tiles = pickle.load(data_ground)
		except:
			self.list_tiles = [[]]

		self.images_tiles = [pygame.image.load(img).convert_alpha() for img in glob.glob(f'Content/Textures/Tiles/*.png')]
		self.resize_tile = (self.size_tile, self.size_tile)
		self.images_tiles = [pygame.transform.scale(img, self.resize_tile) for img in self.images_tiles]
		self.image_ground = self.images_tiles[self.idx_tile]

		self.image_remove_tile = pygame.image.load('Content/Textures/remove_tile.png').convert_alpha()
		self.image_remove_tile = pygame.transform.scale(self.image_remove_tile, self.resize_tile)

		self.image_focus_tile = pygame.image.load('Content/Textures/focus_tile.png').convert_alpha()
		self.image_focus_tile = pygame.transform.scale(self.image_focus_tile, self.resize_tile)

		# Meshs
		with open('Content/Textures/meshs.dll', encoding='utf-8') as infos_mesh:
			self.list_infos_mesh = infos_mesh.read().splitlines()

		self.list_mesh = []
		self.list_model = []
		self.list_file = []
		self.list_location = []

		for mesh in self.list_infos_mesh:
			list_info = mesh.split(', ')
			self.list_mesh.append(list_info[0])
			self.list_model.append(int(list_info[1]))
			self.list_file.append(list_info[2])
			self.list_location.append(list_info[3])

		self.wait_action = False
		self.wait_action_ground = False
		self.wait_action_level = False
		self.wait_action_move_mesh = False
		self.wait_action_enter = False
		self.wait_action_delete = False
		self.wait_action_remove = False
		self.wait_flip_tile = False

	def load_mesh_image(self):
		if self.list_file[self.idx_mesh] == 'file':
			self.image = pygame.image.load('Content/Textures/' + self.list_location[self.idx_mesh] + str(10+self.idx_model) + '.png').convert_alpha()
			self.image_original = pygame.image.load('Content/Textures/' + self.list_location[self.idx_mesh] + str(10+self.idx_model) + '.png').convert_alpha()
		else:
			self.image = pygame.image.load('Content/Textures/' + self.list_location[self.idx_mesh] + str(10+self.idx_model) + '/10.png').convert_alpha()
			self.image_original = pygame.image.load('Content/Textures/' + self.list_location[self.idx_mesh] + str(10+self.idx_model) + '/10.png').convert_alpha()

		self.size_image = self.image.get_size()
		self.resize = (self.size_image[0]*5, self.size_image[1]*5)

		self.image = pygame.transform.scale(self.image, self.resize)
		self.image_original = pygame.transform.scale(self.image, self.resize)

		self.rect = self.image.get_rect()
		self.image.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_MULT)

	def show_hud(self, meshs_blit):
		self.text_title = self.font.render('EDITOR MODE', 1, pygame.Color('red'))
		xy_fps_text = self.text_title.get_size()
		self.screen.blit(self.text_title, (2,20+xy_fps_text[1]*8))

		if self.mode == 'MESH':
			list_text_editor = [
			' - Left clic > Confirm position',
			' - Mouse scroll > Change model of the mesh',
			' - Arrows Left/Right > Change the selected mesh',
			' - Press G > Ground mode',
			f'Mesh selection: {self.list_mesh[self.idx_mesh]} {self.idx_mesh}/{len(self.list_mesh)-1}',
			f'Mesh model: {self.idx_model}/{self.list_model[self.idx_mesh]}',
			f'Len group: {len(meshs_blit)+len(self.list_new_mesh)} meshs']

		elif self.mode == 'GROUND':
			list_text_editor = [
			' - Arrows Left > Change tile angle',
			' - Arrows Up/Down > Change placement level',
			' - Press V > View tiles on the current level',
			' - Press M > Mesh mode',
			f'Tile selection: {self.idx_tile}/{len(self.images_tiles)-1}',
			f'Level: {self.level_tile}',
			f'(Press R) Remove mode: {self.remove_ground_mode}',
			f'(Press F) Flip mode: {self.flip_image}']

			try:
				size_list_tile = len(self.list_tiles[self.level_tile])
			except IndexError:
				size_list_tile = 0
			
			list_text_editor.append(f'Len group in the current level: {size_list_tile} tiles')

		list_text_editor = ['Shortcuts:', ' - F8 > Save map', ' - Right clic > Back to previous action'] + list_text_editor
		list_text_editor.append(self.txt_map_saved)
		self.idx_text_editor = 9

		for text in list_text_editor:
			self.text_save_map = self.font.render(text, 1, pygame.Color('white'))
			self.screen.blit(self.text_save_map, (2,20+xy_fps_text[1]*self.idx_text_editor))
			self.idx_text_editor += 1

	def show(self, Keys, MouseEvent, mouse_position, x, y):
		# Mouse position correction
		self.xy_move_map = (self.xy_move_map[0]+x, self.xy_move_map[1]+y)
		mouse_position = (mouse_position[0]-self.xy_move_map[0], mouse_position[1]-self.xy_move_map[1])

		# Editor mode
		if Keys[pygame.K_g]:
			self.mode = 'GROUND'
		elif Keys[pygame.K_m]:
			self.mode = 'MESH'

		# Mesh
		if self.mode == 'MESH':
			# Change model
			if 'SCROLLDOWN' in MouseEvent:
				if self.idx_model > 0:
					self.idx_model -= 1
					self.load_mesh_image()

			elif 'SCROLLUP' in MouseEvent:
				if self.idx_model < self.list_model[self.idx_mesh]:
					self.idx_model += 1
					self.load_mesh_image()

			# Change mesh
			if Keys[pygame.K_LEFT] and self.wait_action == False:
				if self.idx_mesh > 0:
					self.idx_mesh -= 1
					self.idx_model = 0
					self.wait_action = True
					self.load_mesh_image()

			elif Keys[pygame.K_RIGHT] and self.wait_action == False:
				if self.idx_mesh < len(self.list_mesh)-1:
					self.idx_mesh += 1
					self.idx_model = 0
					self.wait_action = True
					self.load_mesh_image()

			elif Keys[pygame.K_LEFT] == False and Keys[pygame.K_RIGHT] == False:
				self.wait_action = False

		# Ground
		elif self.mode == 'GROUND':
			# Change model
			if 'SCROLLDOWN' in MouseEvent:
				if self.idx_tile > 0:
					self.idx_tile -= 1
					self.image_ground = self.images_tiles[self.idx_tile]
					self.angle_tile = 0
					self.flip_image = False

			elif 'SCROLLUP' in MouseEvent:
				if self.idx_tile < len(self.images_tiles)-1:
					self.idx_tile += 1
					self.image_ground = self.images_tiles[self.idx_tile]
					self.angle_tile = 0
					self.flip_image = False

			# Rotation image
			if Keys[pygame.K_LEFT] and self.wait_action_ground == False:
				if self.angle_tile != 360:
					self.angle_tile += 90
				else:
					self.angle_tile = 90

				self.image_ground = pygame.transform.rotate(self.image_ground, 90)
				self.wait_action_ground = True

			elif Keys[pygame.K_LEFT] == False:
				self.wait_action_ground = False

			# Flip image
			if Keys[pygame.K_f] and self.wait_flip_tile == False:
				if self.flip_image:
					self.flip_image = False
				else:
					self.flip_image = True

				self.image_ground = pygame.transform.flip(self.image_ground, True, False)
				self.wait_flip_tile = True

			elif Keys[pygame.K_f] == False:
				self.wait_flip_tile = False

			# Change level
			if Keys[pygame.K_UP] and self.wait_action_level == False:
				self.level_tile += 1
				self.wait_action_level = True

			elif Keys[pygame.K_DOWN] and self.wait_action_level == False:
				if self.level_tile != 0:
					self.level_tile -= 1
					self.wait_action_level = True

			elif Keys[pygame.K_UP] == False and Keys[pygame.K_DOWN] == False:
				self.wait_action_level = False

			# Remove Mode
			if Keys[pygame.K_r] and self.wait_action_remove == False:
				if self.remove_ground_mode:
					self.remove_ground_mode = False
				else:
					self.remove_ground_mode = True

				self.wait_action_remove = True
			
			elif Keys[pygame.K_r] == False:
				self.wait_action_remove = False


		# Position
		if self.mode == 'MESH':
			self.xy = (int(mouse_position[0]/self.size_tile), int(mouse_position[1]/self.size_tile))
		elif self.mode == 'GROUND':
			self.xy = (int(mouse_position[0]/self.size_tile), int(mouse_position[1]/self.size_tile))

		# Validation position
		if 'LEFTCLIC' in MouseEvent:
			# Mesh
			if self.mode == 'MESH':
				self.list_new_mesh.append([self.list_mesh[self.idx_mesh], self.idx_model, self.xy, self.image_original, self.rect])
				self.txt_map_saved = 'Map not saved'

			# Ground
			elif self.mode == 'GROUND':
				# Remove old tile for the new
				try:
					for index_tile, tile in enumerate(self.list_tiles[self.level_tile]):
						if tile[1] == self.xy:
							del self.list_tiles[self.level_tile][index_tile]
				except IndexError:
					# The list is not long enough and we must add levels to it
					while True:
						try:
							test_value = self.list_tiles[self.level_tile]
							break
						except IndexError:
							self.list_tiles.append([])

				# Append the new tile to display
				if self.remove_ground_mode == False:
					self.list_tiles[self.level_tile].append([self.idx_tile, self.xy, self.angle_tile, self.flip_image])
				
				self.txt_map_saved = 'Map not saved'

		# Delete last mesh
		if self.mode == 'MESH':
			if 'RIGHTCLIC' in MouseEvent:
				if self.wait_action_delete == False and self.list_new_mesh != []:
					del self.list_new_mesh[-1]
					self.wait_action_delete = True
			else:
				self.wait_action_delete = False

		# Display tiles
		for index_level, level in enumerate(self.list_tiles):
			for tile in level:
				position_tile = (tile[1][0]*self.size_tile+self.xy_move_map[0], tile[1][1]*self.size_tile+self.xy_move_map[1])
				image_rotate_tile = pygame.transform.flip(self.images_tiles[tile[0]], tile[3], False)
				image_rotate_tile = pygame.transform.rotate(image_rotate_tile, tile[2])
				self.screen.blit(image_rotate_tile, position_tile)

				# Focus tile if it's on the current level
				if Keys[pygame.K_v] and self.mode == 'GROUND' and index_level == self.level_tile:
					self.screen.blit(self.image_focus_tile, position_tile)

				if Keys[pygame.K_F10]:
					pygame.draw.line(self.screen, 'grey', position_tile, (position_tile[0]+self.size_tile, position_tile[1]))
					pygame.draw.line(self.screen, 'grey', position_tile, (position_tile[0], position_tile[1]+self.size_tile))

		# Display new meshs
		for mesh in self.list_new_mesh:
			xy_mesh_blit = mesh[2][0]*self.size_tile+self.xy_move_map[0], mesh[2][1]*self.size_tile+self.xy_move_map[1]
			self.screen.blit(mesh[3], xy_mesh_blit)

		# Display mesh
		if self.mode == 'MESH':
			try:
				self.xy_mouse_tile_map = (self.xy[0]*self.size_tile+self.xy_move_map[0], self.xy[1]*self.size_tile+self.xy_move_map[1]-1)
				self.screen.blit(self.image, (self.xy_mouse_tile_map[0], self.xy_mouse_tile_map[1]))

			except AttributeError:
				print('ERROR BLIT: (Re)load image to display')
				self.load_mesh_image()

		elif self.mode == 'GROUND':
			self.xy_mouse_tile_map = (self.xy[0]*self.size_tile+self.xy_move_map[0], self.xy[1]*self.size_tile+self.xy_move_map[1])

			if self.remove_ground_mode == False:
				self.screen.blit(self.image_ground, self.xy_mouse_tile_map)

			else:
				self.screen.blit(self.image_remove_tile, self.xy_mouse_tile_map)

		# Save map
		if Keys[pygame.K_F8] and self.txt_map_saved == 'Map not saved':
			# Ground
			with open(f'Content/Maps/{self.name_map}/ground.plk', 'wb') as data_ground:
				pickle.dump(self.list_tiles, data_ground, pickle.HIGHEST_PROTOCOL)

			# Meshs
			with open(f'Content/Maps/{self.name_map}/landscape.maps') as ancient_mesh:
				list_ancient_mesh = ancient_mesh.read().splitlines()

			file_save = open(f'Content/Maps/{self.name_map}/landscape.maps', 'w')
			file_bin = open(f'Content/Maps/{self.name_map}/bin.maps', 'w')

			for mesh in list_ancient_mesh:
				file_save.write(f'{mesh}\n')
				file_bin.write(f'{mesh}\n')

			file_bin.close()

			for mesh in self.list_new_mesh:
				file_save.write(f'{mesh[0]} | {mesh[1]+10}, {int(mesh[2][0])};{int(mesh[2][1])}\n')

			file_save.close()
			self.txt_map_saved = 'Map saved'