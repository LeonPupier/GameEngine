import pygame, glob, os
from random import randint

from interaction import *

class Widgets():
	def __init__(self):
		self.list_widgets = []

######################################################################################################################################################

class Logo():
	def __init__(self, screen, size, interaction_class):
		self.screen = screen
		self.size = size
		self.interaction_class = interaction_class

		self.time_show_logo = 0
		self.duration_logo = 6

		self.image_logo = pygame.image.load('Content/Ui/logo.png').convert_alpha()
		self.size_image_logo = self.image_logo.get_size()
		self.resize_logo = (int((size[0]*self.size_image_logo[0]*10)/1920), int((size[1]*self.size_image_logo[1]*10)/1080))
		self.image_logo = pygame.transform.scale(self.image_logo, self.resize_logo)

		self.xy_logo = (size[0]/2-self.resize_logo[0]/2, size[1]/2-self.resize_logo[1]/2)
		self.opacity_logo = 0
		self.image_logo.set_alpha(self.opacity_logo)

		self.interaction_class.play_sound('logo', volume_sound=1)

	def show(self):
		dt = float(os.environ['DELTA_TIME'])

		if self.opacity_logo < 255:
			self.opacity_logo += 5
			self.image_logo.set_alpha(self.opacity_logo)

		if self.time_show_logo >= self.duration_logo/2:
			self.opacity_logo -= 7
			self.image_logo.set_alpha(self.opacity_logo)

		pygame.draw.rect(self.screen, 'white', (0,0,self.size[0], self.size[1]))
		self.screen.blit(self.image_logo, self.xy_logo)

		if self.time_show_logo >= self.duration_logo:
			return 'end_logo'
		self.time_show_logo += dt

######################################################################################################################################################

class Loading():
	def __init__(self, screen, size, save_class):
		self.screen = screen
		self.size = size

		self.image_loading = pygame.image.load('Content/Ui/loading/' + str(randint(10, 10)) + '.png').convert_alpha()
		self.resize = (int((size[0]*1920)/1920), int((size[1]*1080)/1080))
		self.image_loading = pygame.transform.scale(self.image_loading, self.resize)

		self.size_font_loading = int((size[0]*40)/1600)
		self.font_loading = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font_loading)

		text = save_class.load_language('ui')[0]
		self.text_loading1 = text + '.'
		self.text_loading2 = text + '..'
		self.text_loading3 = text + '...'

		self.text_loading_render = []
		self.text_loading_render.append(self.font_loading.render(self.text_loading1, self.size_font_loading, pygame.Color('white')))
		self.text_loading_render.append(self.font_loading.render(self.text_loading2, self.size_font_loading, pygame.Color('white')))
		self.text_loading_render.append(self.font_loading.render(self.text_loading3, self.size_font_loading, pygame.Color('white')))

		self.idx = 0
		self.fps_count = 0
		self.time_animation = 0.8
		self.coordonnee_loading = self.text_loading_render[2].get_size()

	def show(self):
		dt = float(os.environ['DELTA_TIME'])

		self.fps_count += dt
		if 0 <= self.fps_count <= self.time_animation:
			self.idx = 0
		elif self.time_animation < self.fps_count <= self.time_animation*2:
			self.idx = 1
		elif self.time_animation*2 < self.fps_count <= self.time_animation*3:
			self.idx = 2
		else:
			self.fps_count = 0

		self.screen.blit(self.image_loading, (0, 0))
		self.screen.blit(self.text_loading_render[self.idx], (self.size[0]-self.coordonnee_loading[0]*1.05, self.size[1]-self.coordonnee_loading[1]))

######################################################################################################################################################

class MainMenu():
	def __init__(self, screen, size, sound, language_ui):
		self.screen = screen
		self.size = size
		self.language_ui = language_ui

		self.text_color = 'black'
		self.size_font = int((size[0]*30)/1600)
		self.size_font_version = int((size[0]*20)/1600)
		self.font = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font)
		self.font_version = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font_version)

		self.resize_background = size
		self.image_background = pygame.image.load('Content/Maps/main_menu/0.png').convert_alpha()
		self.image_background = pygame.transform.scale(self.image_background, self.resize_background)

		# PNJ
		self.image_u = pygame.image.load('Content/Textures/Characters/0/u.png').convert_alpha()
		self.size_default = self.image_u.get_size()
		self.resize_pnj = (int((size[0]*self.size_default[0]*6)/1920), int((size[1]*self.size_default[1]*6)/1080))
		self.image_u = pygame.transform.scale(self.image_u, self.resize_pnj)

		self.image_u1 = pygame.image.load('Content/Textures/Characters/0/u1.png').convert_alpha()
		self.image_u1 = pygame.transform.scale(self.image_u1, self.resize_pnj)

		self.image_u2 = pygame.image.load('Content/Textures/Characters/0/u2.png').convert_alpha()
		self.image_u2 = pygame.transform.scale(self.image_u2, self.resize_pnj)

		self.image_shadow = pygame.image.load('Content/Textures/Characters/Player/shadow.png').convert_alpha()
		self.image_shadow = pygame.transform.scale(self.image_shadow, self.resize_pnj)

		self.list_pnj_walk = [self.image_u, self.image_u1, self.image_u2]
		self.time_animation_walking = 0.3
		self.fps_count_walk = 0
		self.idx_walking = 0
		self.xy_pnj_walk = (size[0]/18*12, size[1]/2)
		
		# Board button
		self.image_board_button = pygame.image.load('Content/Ui/hud/text_button.png').convert_alpha()

		# Bird loading
		self.images_bird = [pygame.image.load(img).convert_alpha() for img in glob.glob('Content/Textures/Characters/2/*.png')]
		self.size_image_bird = self.images_bird[0].get_size()
		self.resize_bird = (int((self.size[0]*self.size_image_bird[0]*5)/1920), int((self.size[1]*self.size_image_bird[1]*5)/1080))
		self.images_bird = [pygame.transform.scale(self.image, self.resize_bird) for self.image in self.images_bird]

		self.fps_time_bird = 5
		self.time_show_bird = 15
		self.show_bird = False
		self.index_bird = 0
		self.change_animation_bird = 0.33
		self.time_animation_bird = 0

		self.speed_background = size[0]*0.2/1600
		self.list_xy_background = [(0,0), (0,-self.size[1])]
		self.xy_transition = (0,0)

		self.x_text = self.size[0]/20
		self.y_text = self.size[1]/3*2

		# Text Buttons
		self.text_newgame = self.language_ui[1]
		self.text_load = self.language_ui[2]
		self.text_settings = self.language_ui[3]
		self.text_quit = self.language_ui[4]

		self.render_newgame = self.font.render(self.text_newgame, self.size_font, pygame.Color(self.text_color))
		self.render_load = self.font.render(self.text_load, self.size_font, pygame.Color(self.text_color))
		self.render_settings = self.font.render(self.text_settings, self.size_font, pygame.Color(self.text_color))
		self.render_quit = self.font.render(self.text_quit, self.size_font, pygame.Color(self.text_color))

		self.size_newgame = self.render_newgame.get_size()

		self.resize_board_button = (int(self.size_newgame[0]), int(self.size_newgame[1]))
		self.image_board_button = pygame.transform.scale(self.image_board_button, (self.resize_board_button[0]*1.3, self.resize_board_button[1]))

		self.sound = sound
		self.play_transition = True

		# Version info
		self.render_game_version = self.font_version.render(os.environ['GAME_VERSION'], self.size_font_version, pygame.Color('white'))
		self.size_render_version = self.render_game_version.get_size()
		self.xy_version_game = (self.size[0]-self.size_render_version[0], self.size[1]-self.size_render_version[1])

	def show(self, x_mouse, y_mouse):
		dt = float(os.environ['DELTA_TIME'])

		if self.play_transition:
			self.sound.play_sound('transition_logo')
			self.play_transition = False

		del_element = False
		for index_background_image, background_image in enumerate(self.list_xy_background):

			# If the image is out of the screen
			if background_image[1] >= self.size[1]:
				del_element = True
			else:
				self.list_xy_background[index_background_image] = (background_image[0], background_image[1]+self.speed_background)
			
			self.screen.blit(self.image_background, background_image)

		if del_element:
			self.list_xy_background.pop(0)
			self.list_xy_background.append((0,-self.size[1]+self.speed_background))

		if self.fps_time_bird >= self.time_show_bird:
			self.show_bird = True
			self.xy_bird = (-self.resize_bird[0], randint(0,self.size[1]*1.5))
			self.fps_time_bird = 0
		else:
			self.fps_time_bird += dt

		# Bird fly animation
		if self.show_bird:
			if self.time_animation_bird >= self.change_animation_bird:
				self.time_animation_bird = 0
				self.index_bird += 1
			else:
				self.time_animation_bird += dt

			self.xy_bird = (self.xy_bird[0]+(self.size[0]*2)/1600, self.xy_bird[1]-(self.size[0]*1)/1600)

			try:
				self.screen.blit(self.images_bird[self.index_bird], self.xy_bird)
			except IndexError:
				self.index_bird = 0
				self.screen.blit(self.images_bird[self.index_bird], self.xy_bird)

			if self.xy_bird[0] >= self.size[0] and self.xy_bird[1] >= self.size[1]:
				self.show_bird = False

		# Text buttons
		self.screen.blit(self.image_board_button, (self.x_text/1.5, self.y_text+self.size_newgame[1]/8))
		self.screen.blit(self.render_newgame, (self.x_text, self.y_text))

		self.screen.blit(self.image_board_button, (self.x_text/1.5, self.y_text+self.size_newgame[1]*1.6))
		self.screen.blit(self.render_load, (self.x_text, self.y_text+self.size_newgame[1]*1.5))

		self.screen.blit(self.image_board_button, (self.x_text/1.5, self.y_text+self.size_newgame[1]*3.1))
		self.screen.blit(self.render_settings, (self.x_text, self.y_text+self.size_newgame[1]*3))

		self.screen.blit(self.image_board_button, (self.x_text/1.5, self.y_text+self.size_newgame[1]*4.6))
		self.screen.blit(self.render_quit, (self.x_text, self.y_text+self.size_newgame[1]*4.5))

		# Pnj walking
		if self.fps_count_walk >= self.time_animation_walking:
			if self.idx_walking < len(self.list_pnj_walk)-1:
				self.idx_walking += 1
			else:
				self.idx_walking = 0
			self.fps_count_walk = 0
		else:
			self.fps_count_walk += dt

		self.screen.blit(self.image_shadow, self.xy_pnj_walk)
		self.screen.blit(self.list_pnj_walk[self.idx_walking], self.xy_pnj_walk)

		# Game version infp
		self.screen.blit(self.render_game_version, self.xy_version_game)

		# Transition
		if self.xy_transition[1] <= self.size[1]:
			pygame.draw.rect(self.screen, 'white', (self.xy_transition[0], self.xy_transition[1], self.size[0], self.size[1]))
			self.xy_transition = (self.xy_transition[0], self.xy_transition[1]+(self.size[0]*20)/1600)

######################################################################################################################################################

class HUD():
	def __init__(self, screen, size, save_class):
		self.screen = screen
		self.size = size
		self.time_scrolling = 2
		self.fps_scrolling = 0
		self.save_class = save_class

		self.text_color = 'black'
		self.color_quests = '#C33606'

		self.size_font = int((size[0]*30)/1600)
		self.size_font_quests_label = int((size[0]*20)/1600)
		self.size_font_quests_infos = int((size[0]*20)/1600)
		self.font = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font)
		self.font_quests = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font_quests_label)
		self.font_quest_infos = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font_quests_infos)

		self.image_bar = pygame.image.load('Content/Ui/hud/bar.png').convert_alpha()
		self.size_image_bar = self.image_bar.get_size()
		self.resize_bar = (int((size[0]*self.size_image_bar[0]*5)/1920), int((size[1]*self.size_image_bar[1]*5)/1080))
		self.image_bar = pygame.transform.scale(self.image_bar, self.resize_bar)

		self.image_quest = pygame.image.load('Content/Ui/hud/quest.png').convert_alpha()
		self.size_image_quests = self.image_quest.get_size()

		self.image_task_check_true = pygame.image.load('Content/Ui/hud/task_true.png').convert_alpha()
		self.image_task_check_false = pygame.image.load('Content/Ui/hud/task_false.png').convert_alpha()

		self.size_task_check = self.image_task_check_true.get_size()
		self.resize_task_check = (int((size[0]*self.size_task_check[0]*2)/1920), int((size[1]*self.size_task_check[1]*2)/1080))

		self.image_task_check_true = pygame.transform.scale(self.image_task_check_true, self.resize_task_check)
		self.image_task_check_false = pygame.transform.scale(self.image_task_check_false, self.resize_task_check)
		self.size_task_check = self.image_task_check_true.get_size()

		self.idx_main = 3
		self.idx_side = 0

		self.xy_bar = (size[0]-self.resize_bar[0], 0)

		self.size_pixel = size[0]*6/1600

		self.focus_shadows = False
		self.image_shadows = pygame.image.load('Content/Ui/hud/shadows.png').convert_alpha()
		self.resize_shadows = (int(size[0]), int(size[1]))
		self.image_shadows = pygame.transform.scale(self.image_shadows, self.resize_shadows)

		self.focus_blurry = False
		self.image_blurry = pygame.image.load('Content/Ui/hud/blurry.png').convert_alpha()
		self.resize_blurry = (int(size[0]), int(size[1]))
		self.image_blurry = pygame.transform.scale(self.image_blurry, self.resize_blurry)

		# Disclaimer
		self.image_disclaimer = pygame.image.load('Content/Ui/hud/disclaimer.png').convert_alpha()
		self.size_image_disclaimer = self.image_disclaimer.get_size()
		self.resize_disclaimer = (int((size[0]*self.size_image_disclaimer[0]*0.55)/1920), int((size[1]*self.size_image_disclaimer[1]*0.55)/1080))
		self.image_disclaimer = pygame.transform.scale(self.image_disclaimer, self.resize_disclaimer)
		self.xy_disclaimer = (3, 3)

	def show(self, scroll='center', editor='not_init'):
		dt = float(os.environ['DELTA_TIME'])

		if scroll == 'up' and self.xy_bar[1] > -self.resize_bar[1]:
			self.xy_bar = (self.xy_bar[0], self.xy_bar[1]-self.time_scrolling*2)
			self.fps_scrolling = 0

		elif scroll == 'down' and self.xy_bar[1] < 0:
			if self.fps_scrolling >= 1:
				self.xy_bar = (self.xy_bar[0], self.xy_bar[1]+self.time_scrolling)
			else:
				self.fps_scrolling += dt

		# Functions
		level = str(self.save_class.list_save[0][11])
		nb_money = str(self.save_class.list_save[0][10])
		quest_title = self.save_class.list_save[2][0]
		quest_infos = self.save_class.list_save[2][1]

		# Quest title
		self.quest_title = self.font_quests.render(quest_title, self.size_font_quests_label, pygame.Color(self.color_quests))
		size_quest_title = self.quest_title.get_size()
		
		self.resize_quests = (size_quest_title[0]*1.05, int((self.size[1]*self.size_image_quests[1]*5)/1080))
		self.image_quest = pygame.transform.scale(self.image_quest, self.resize_quests)
		size_image_quest = self.image_quest.get_size()

		self.xy_quest = (self.size[0]-size_image_quest[0], self.xy_bar[1]+self.resize_bar[1]*1.1)
		self.xy_quest_title = (self.size[0]-size_quest_title[0]*1.02, self.xy_quest[1])

		# Money
		self.text_money = self.font.render(nb_money, self.size_font, pygame.Color(self.text_color))
		size_text_money = self.text_money.get_size()
		position_text_money = (self.xy_bar[0]+self.resize_bar[0]/1.17-size_text_money[0]/2, self.xy_bar[1]+self.resize_bar[1]/5)

		# DISPLAY PART
		if editor == 'not_init':
			# Shadows
			if self.focus_shadows == True:
				self.screen.blit(self.image_shadows, (0, 0))

			# Blurry
			elif self.focus_blurry == True:
				self.screen.blit(self.image_blurry, (0, 0))

			# Player panel top right
			self.screen.blit(self.image_bar, self.xy_bar)

			# Display money
			self.screen.blit(self.text_money, position_text_money)

			# Quest image and title
			self.screen.blit(self.image_quest, self.xy_quest)
			self.screen.blit(self.quest_title, self.xy_quest_title)

			# Display heart bar
			self.size_bg_heart_bar = (self.xy_bar[0]+self.resize_bar[0]/5.5, self.xy_bar[1]+(self.resize_bar[1]/10*7.1), self.size_pixel*30, self.size_pixel*3)
			pygame.draw.rect(self.screen, '#B23E00', self.size_bg_heart_bar)

			self.size_model_heart_bar = (self.xy_bar[0]+self.resize_bar[0]/5.5+self.size_pixel, self.xy_bar[1]+(self.resize_bar[1]/10*7.1)+self.size_pixel, self.size_pixel*28, self.size_pixel)
			pygame.draw.rect(self.screen, '#D84B00', self.size_model_heart_bar)

			self.size_heart_bar = (self.xy_bar[0]+self.resize_bar[0]/5.5+self.size_pixel, self.xy_bar[1]+(self.resize_bar[1]/10*7.1)+self.size_pixel, self.size_pixel*18, self.size_pixel)
			pygame.draw.rect(self.screen, '#1AA022', self.size_heart_bar)

			# Display level bar and infos
			self.size_bg_level_bar = (self.xy_bar[0]+self.resize_bar[0]/5.5, self.xy_bar[1]+(self.resize_bar[1]/10*8.4), self.size_pixel*30, self.size_pixel*3)
			pygame.draw.rect(self.screen, '#B23E00', self.size_bg_level_bar)

			self.size_model_level_bar = (self.xy_bar[0]+self.resize_bar[0]/5.5+self.size_pixel, self.xy_bar[1]+(self.resize_bar[1]/10*8.4)+self.size_pixel, self.size_pixel*28, self.size_pixel)
			pygame.draw.rect(self.screen, '#D84B00', self.size_model_level_bar)

			self.size_level_bar = (self.xy_bar[0]+self.resize_bar[0]/5.5+self.size_pixel, self.xy_bar[1]+(self.resize_bar[1]/10*8.4)+self.size_pixel, self.size_pixel*9, self.size_pixel)
			pygame.draw.rect(self.screen, '#3C3CB8', self.size_level_bar)

			self.text_level = self.font_quests.render(level, self.size_font_quests_infos, pygame.Color('black'))
			self.xy_text_level = (self.xy_bar[0]+self.resize_bar[0]/9.5, self.xy_bar[1]+(self.resize_bar[1]/10*8))
			self.screen.blit(self.text_level, self.xy_text_level)

			# Quest infos
			y_text_task = self.xy_quest[1]
			for quest in quest_infos.items():
				text_task, value_task = quest

				render_text_task = self.font_quest_infos.render(text_task, self.size_font_quests_infos, pygame.Color('white'))
				size_text_task = render_text_task.get_size()

				y_text_task += size_quest_title[1]*1.2
				xy_quest_task = (self.size[0]-size_text_task[0]-self.size_task_check[0]*1.5, y_text_task)

				self.screen.blit(render_text_task, xy_quest_task)

				# Tasks check
				xy_check = (self.size[0]-self.size_task_check[0]*1.2, y_text_task)
				if value_task:
					self.screen.blit(self.image_task_check_true, xy_check)
				else:
					self.screen.blit(self.image_task_check_false, xy_check)

			# Disclaimer: Work in progress
			self.screen.blit(self.image_disclaimer, self.xy_disclaimer)

######################################################################################################################################################

class Menu():
	def __init__(self, screen, size, widgets_class, interaction_class):
		self.screen = screen

		self.text_color = 'black'
		self.size_font = int((size[0]*30)/1600)
		self.font = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font)

		self.image_menu = pygame.image.load('Content/Ui/hud/menu_background.png').convert_alpha()
		self.resize_menu = (int(size[0]), int(size[1]))
		self.image_menu = pygame.transform.scale(self.image_menu, self.resize_menu)

		self.xy_menu = (0, 0)

		# Widgets
		self.widgets_class = widgets_class
		self.entry1 = Entry(self.screen, size, 7, 60, (250,400), interaction_class)

	def show(self, Keys):
		self.screen.blit(self.image_menu, self.xy_menu)

		if self.entry1 not in self.widgets_class.list_widgets:
			self.widgets_class.list_widgets.append(self.entry1)
		self.entry1.show(Keys)

######################################################################################################################################################

class Entry():
	def __init__(self, screen, size, scale_y, scale_middle, position, interaction_class, colors=None):
		self.screen = screen
		self.size = size
		self.interaction_class = interaction_class
		self.scale_y = scale_y
		self.position = position

		self.size_font = int((size[0]*25)/1600)
		self.font = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font)

		# Rect entry borders
		self.resize_side = (int((size[0]*scale_y)/1920), int((size[1]*(10*scale_y))/1080))
		self.xy_pixel_entry = int((size[0]*5)/1920)
		self.xy_rect_internal = (position[0], position[1], scale_middle*self.xy_pixel_entry, scale_y*self.xy_pixel_entry)
		self.xy_rect_external = (
			position[0]-self.xy_pixel_entry,
			position[1]-self.xy_pixel_entry,
			scale_middle*self.xy_pixel_entry+self.xy_pixel_entry*2,
			scale_y*self.xy_pixel_entry+self.xy_pixel_entry*2)

		self.rect = pygame.Rect(self.xy_rect_internal)

		# Customizable colors
		if colors != None:
			self.color_rect_internal, self.color_rect_external, self.color_rect_external_focus, self.color_line, self.color_text = colors
		else:
			self.color_rect_internal = 'white'
			self.color_rect_external = 'grey'
			self.color_rect_external_focus = '#7D7D7D'
			self.color_line = 'black'
			self.color_text = 'black'

		# Size of a letter
		self.text_little = self.font.render('a', self.size_font, pygame.Color('black')) # Minuscule
		self.text_big = self.font.render('A', self.size_font, pygame.Color('black')) # Big
		self.size_little_letter = self.text_little.get_size()
		self.size_big_letter = self.text_big.get_size()

		# Entry data
		self.text_entry = ''
		self.fps_count_line = 0
		self.time_line = 0.8
		self.ancien_key = None
		self.focus_entry = False

	def clic_mouse(self, clic):
		if clic == 'left' and self.focus_entry == False:
			self.focus_entry = True

	def no_clic_mouse(self):
		self.focus_entry = False

	def show(self, Keys):
		dt = float(os.environ['DELTA_TIME'])

		if self.focus_entry:
			pygame.draw.rect(self.screen, self.color_rect_external_focus, self.xy_rect_external)
		else:
			pygame.draw.rect(self.screen, self.color_rect_external, self.xy_rect_external)

		pygame.draw.rect(self.screen, self.color_rect_internal, self.xy_rect_internal)

		if self.focus_entry == True:
			# Insert text
			key_pressed = self.interaction_class.detect_keys(Keys)

			# Standard key
			if key_pressed not in (None, self.ancien_key, 'backspace') and self.xy_line[0]+self.size_big_letter[0] < self.position[0]+self.xy_rect_internal[2]:
				self.text_entry += key_pressed
				self.ancien_key = key_pressed

			if key_pressed == None:
				self.ancien_key = None

			if key_pressed == 'backspace':
				if self.ancien_key != key_pressed:
					self.text_entry = self.text_entry[:-1]
				self.ancien_key = key_pressed

			self.xy_line = (self.rect.x + self.text_entry_render.get_size()[0], self.rect.y, self.xy_pixel_entry, self.scale_y*self.xy_pixel_entry)

		self.xy_text = (self.rect[0], self.rect[1])
		self.text_entry_render = self.font.render(self.text_entry, self.size_font, pygame.Color(self.color_text))

		self.screen.blit(self.text_entry_render, self.xy_text)

		if self.focus_entry == True:
			if 0 <= self.fps_count_line <= self.time_line:
				pygame.draw.rect(self.screen, self.color_line, self.xy_line)
				self.fps_count_line += dt
			elif self.time_line < self.fps_count_line < self.time_line*2:
				self.fps_count_line += dt
			elif self.fps_count_line >= self.time_line*2:
				self.fps_count_line = 0

######################################################################################################################################################

class NewGame():
	def __init__(self, screen, size):
		self.screen = screen

	def setup(self, screen):
		pass