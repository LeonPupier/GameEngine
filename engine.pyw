# Hide pygame support
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame, sys, configparser, socket, time, shutil
import platform as plt
from pygame.locals import *
import OpenGL
import psutil, logging

from ui import *
from map import *
from player import *
from interaction import *
from editor import *
from save import *
from effects import World_Effect

# Initialisation log system
open('Content/engine.log', 'w').close()
logging.basicConfig(filename='Content/engine.log', level=logging.DEBUG)
logging.debug('Successful import of internal and external modules')

# Computer informations
list_infos = [socket.gethostname(), plt.system(), sys.platform, plt.machine(), plt.platform(), plt.release(), plt.version(), plt.processor()]

list_explication = ['Name machine', 'System OS', 'System machine', 'Machine', 'Platforme',
					'Release', 'Version', 'Processor', 'SDL version', 'Mixer version',
					'Display driver', 'Screen size', 'SDL flags']

for nb_infos in range(len(list_infos)):
	explication = f'{list_explication[nb_infos]}: {list_infos[nb_infos]}'
	logging.debug(explication)

# Digital Rights Management (DRM)
try:
	title = os.environ['GAME_TITLE']
	version = os.environ['GAME_VERSION']
	logging.debug('DRM accepted')
except:
	logging.error('Environment variables {title, version} not found and/or DRM not passed')
	sys.exit(0)

# Operating system check
if plt.system() in ('linux', 'linux2', 'linux3'):
	user_os = 'linux'
elif plt.system() in ('win', 'cygwin', 'Windows'):
	user_os = 'windows'
else:
	user_os = plt.system()

if user_os in ('linux', 'windows'):
	path = ''
else:
	logging.error('Operating system not supported')
	sys.exit(0)

# Dev variables
color_dev = 'white'
show_main_menu = False
update_loop = False
debug = False

debug = bool(int(os.environ['DEVMODE']))
editor_mode = bool(int(os.environ['EDITOR']))
show_logo = bool(int(os.environ['SHOW_LOGO']))
if show_logo == False:
	show_main_menu = True

# Initializes external components
pygame.init()
pygame.joystick.init()
logging.debug('Pygame launched')
logging.debug(f'Pygame version: {pygame.version.ver}')
logging.debug(f'Pygame SDL version: {pygame.mixer.get_sdl_mixer_version()}')
logging.debug(f'Pygame display driver: {pygame.display.get_driver()}')

# Engine configuration
config_engine = configparser.ConfigParser()
config_engine.read('Content/engine.ini')

# Infos screen
largeur = config_engine['CONFIG']['Width']
hauteur = config_engine['CONFIG']['Height']
load_flags = (config_engine['CONFIG']['Fullscreen'], config_engine['CONFIG']['DoubleBuff'], config_engine['CONFIG']['HardwareSurface'])
directx = config_engine['CONFIG']['DirectX']
logging.debug(f'DirectX: {directx}')
language = config_engine['CONFIG']['Language']
logging.debug(f'Language: {language}')
vsync = config_engine['CONFIG']['VSync']
logging.debug(f'Vsync: {vsync}')
if vsync == 'True':
	vsync = True
else:
	vsync = False

# Keyboard shortcuts
os.environ['KEYBOARD_ACTION'] = config_engine['KEYBOARD']['Action']
os.environ['KEYBOARD_SIDE_ACTION'] = config_engine['KEYBOARD']['SideAction']
os.environ['KEYBOARD_UP'] = config_engine['KEYBOARD']['Up']
os.environ['KEYBOARD_DOWN'] = config_engine['KEYBOARD']['Down']
os.environ['KEYBOARD_LEFT'] = config_engine['KEYBOARD']['Left']
os.environ['KEYBOARD_RIGHT'] = config_engine['KEYBOARD']['Right']
os.environ['KEYBOARD_INVENTORY'] = config_engine['KEYBOARD']['Inventory']
os.environ['KEYBOARD_MAP'] = config_engine['KEYBOARD']['Map']
os.environ['KEYBOARD_QUEST'] = config_engine['KEYBOARD']['Quest']
os.environ['KEYBOARD_HIDE_WEAPON'] = config_engine['KEYBOARD']['HideWeapon']
os.environ['KEYBOARD_SHOW_WEAPON'] = config_engine['KEYBOARD']['ShowWeapon']
logging.debug('Keyboard actions initialized')

# Controller shortcuts
os.environ['CONTROLLER_MARGE_STICK_LEFT'] = config_engine['CONTROLLER']['MargeStickLeft']
os.environ['CONTROLLER_MARGE_STICK_RIGHT'] = config_engine['CONTROLLER']['MargeStickRight']
os.environ['CONTROLLER_ACTION'] = config_engine['CONTROLLER']['Action']
os.environ['CONTROLLER_SIDE_ACTION'] = config_engine['CONTROLLER']['SideAction']
os.environ['CONTROLLER_RETURN'] = config_engine['CONTROLLER']['Return']
os.environ['CONTROLLER_MOVE'] = config_engine['CONTROLLER']['Move']
os.environ['CONTROLLER_INVENTORY'] = config_engine['CONTROLLER']['Inventory']
os.environ['CONTROLLER_MAP'] = config_engine['CONTROLLER']['Map']
os.environ['CONTROLLER_QUEST'] = config_engine['CONTROLLER']['Quest']
os.environ['CONTROLLER_QUIT'] = config_engine['CONTROLLER']['Quit']
os.environ['CONTROLLER_HIDE_WEAPON'] = config_engine['CONTROLLER']['HideWeapon']
os.environ['CONTROLLER_SHOW_WEAPON'] = config_engine['CONTROLLER']['ShowWeapon']
logging.debug('Controller actions initialized')

# Initialisation screen flags
hardware_acceleration = load_flags[2]
if hardware_acceleration == 'True':
	hardware_acceleration = True
else:
	hardware_acceleration = False

if load_flags == ('True', 'True', 'True'):
	flags = FULLSCREEN | DOUBLEBUF | OPENGL
	logging.debug('Window flags: {FULLSCREEN, DOUBLEBUF, OPENGL}')
elif load_flags == ('False', 'True', 'True'):
	flags = DOUBLEBUF | OPENGL
	logging.debug('Window flags: {DOUBLEBUF, OPENGL}')
elif load_flags == ('True', 'False', 'True'):
	flags = FULLSCREEN | OPENGL
	logging.debug('Window flags: {FULLSCREEN, OPENGL}')
elif load_flags == ('True', 'True', 'False'):
	flags = FULLSCREEN | DOUBLEBUF
	logging.debug('Window flags: {FULLSCREEN, DOUBLEBUF}')
elif load_flags == ('False', 'True', 'False'):
	flags = DOUBLEBUF
	logging.debug('Window flag: DOUBLEBUF')
elif load_flags == ('True', 'False', 'False'):
	flags = FULLSCREEN
	logging.debug('Window flag: FULLSCREEN')
else:
	flags = None
	logging.debug('No window flag')

# Temporary screen init pygame
size = (int(largeur), int(hauteur))
size_tile = size[0]*96/1920
logging.debug(f'Size window: {size}')

if hardware_acceleration:
	pygame.display.set_mode(size, flags, vsync=vsync)
	pygame.display.set_caption(f'{title} v{version}')
	pygame.display.set_icon(pygame.image.load("Content/Ui/icon.png"))
	pygame.display.init()
	info = pygame.display.Info()

	# Basic OpenGL configuration
	glViewport(0, 0, info.current_w, info.current_h)
	glDepthRange(0, 1)
	glMatrixMode(GL_PROJECTION)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glShadeModel(GL_SMOOTH)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_LIGHTING)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	glEnable(GL_BLEND)
	texID = glGenTextures(1)

	# Make the screen window
	screen = pygame.Surface((info.current_w, info.current_h))
	screen_hidden = False

else:
	screen = pygame.display.set_mode(size, flags | pygame.HIDDEN)
	pygame.display.set_caption(f'{title} v{version}')
	pygame.display.set_icon(pygame.image.load("Content/Ui/icon.png"))
	screen_hidden = True

	if directx == 'True':
		pygame.display.init()
		os.environ['SDL_VIDEODRIVER'] = 'directx'

# Assigning environment variables
fps_lock = int(os.environ['FPS'])
fpsClock = pygame.time.Clock()

# Font loading
font_pixel = pygame.font.Font('Content/Fonts/pixel_game.ttf', int((size[0]*20)/1600))
logging.debug("Font 'Content/Fonts/pixel_game.ttf' loaded")

# Function to convert a PyGame Surface to an OpenGL Texture
def surfaceToTexture(pygame_surface):
	global texID
	
	rgb_surface = pygame.image.tostring(pygame_surface, 'RGB')
	glBindTexture(GL_TEXTURE_2D, texID)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

	surface_rect = pygame_surface.get_rect()
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, surface_rect.width, surface_rect.height, 0, GL_RGB, GL_UNSIGNED_BYTE, rgb_surface)
	glGenerateMipmap(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, 0)

# Map loading
def load_map(name_map, save_class):
	global player

	# Effects
	effect = load_effect(screen, size, save_class.list_save[1])

	# Launch map
	if editor_mode:
		editor = Editor(screen, size, size_tile, name_map)
		logging.debug('Editor mode loaded')
		player = load_player(screen, size, save_class.list_save[0], editor)
		map_class = Map(screen, size, name_map, interaction_class, size_tile, save_class, player, editor=True)
		logging.debug('Map loaded')
		return map_class, effect, editor

	else:
		player = load_player(screen, size, save_class.list_save[0], 'not_init')
		map_class = Map(screen, size, name_map, interaction_class, size_tile, save_class, player, editor=False)
		logging.debug('Map loaded')
		return map_class, effect

# Player loading
def load_player(screen, size, save_player, editor):
	logging.debug('Player loaded')
	if editor != 'not_init':
		return Player(screen, size, save_player, True)
	return Player(screen, size, save_player)

def load_effect(screen, size, save_world):
	logging.debug('Effect loaded')
	return World_Effect(screen, size, save_world)

# Initialisation controller
def load_joystick():
	try:
		joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		joystick = pygame.joystick.Joystick(joysticks[0].get_id())
		return joystick

	except IndexError:
		return False

# No joystick found for button binding
class Joystick_Not_Plug():
	def get_button(self, button):
		return False

# Environment
x,y = 0,0
interact_action = False
interact_object = False
add_interact_object = None
fps_count_interact = 0
fps_count_proc = 0
proc_used = 0
idx_interact = 0
enable_move = True
show_menu = False
ancien_mesh_clic = None
fps_count_joystick_reload = 0
x_mouse, y_mouse = 0, 0
map_load_control = True

# Init save class
nb_save = 0
save_class = Save(title, language, nb_save)
path_save = save_class.path()

# Check if a save directory exist on this machine
save_class.check_save_folder()
logging.debug('Try to import the player save...')

# Load save
save_class.load()
logging.debug('Successfully imported')

# Class system
interaction_class = Interaction(screen, size)
logging.debug('Interaction class loaded')
hud_class = HUD(screen, size, save_class)
logging.debug('HUD loaded')
loading = Loading(screen, size, save_class)
logging.debug('Loading loaded')
widgets_class = Widgets()
logging.debug('Widgets loaded')
menu = Menu(screen, size, widgets_class, interaction_class)
logging.debug('Menu loaded')
main_menu = MainMenu(screen, size, interaction_class, save_class.load_language('ui'))
logging.debug('MainMenu loaded')

# Map main menu loading
maps = MapMainMenu()
editor = 'not_init'

# Light loading
light = pygame.image.load('Content/Textures/light.png')
night_mode = False

# Controller
joystick = load_joystick()
joystick_not_plug = Joystick_Not_Plug()

# Cursor loading
pygame.mouse.set_visible(False)

resize_cursor = (int((size[0]*16)/1600), int((size[1]*22)/900))
image_cursor = pygame.image.load('Content/Ui/cursor.png').convert_alpha()
image_cursor = pygame.transform.scale(image_cursor, resize_cursor)
image_cursor_click = pygame.image.load('Content/Ui/cursor_click.png').convert_alpha()
image_cursor_click = pygame.transform.scale(image_cursor_click, resize_cursor)

# Frame update
def update(Keys, MouseEvent):
	global x, y, maps, map_load_control
	global left_clic, middle_clic, right_clic, x_mouse, y_mouse
	global interact_action, interact_object, add_interact_object, fps_count_interact, idx_interact
	global enable_move, show_menu
	global ancien_mesh_clic
	global joystick, fps_count_joystick_reload
	global editor, fps_count_proc, proc_used

	# Collision
	mesh_collision = []
	collision_up, collision_down, collision_left, collision_right = False, False, False, False
	for mesh in maps.group_collision:
		if player.rect_up.colliderect(mesh.rect):
			mesh_collision.append(mesh)
			collision_up = True
		if player.rect_down.colliderect(mesh.rect):
			mesh_collision.append(mesh)
			collision_down = True
		if player.rect_left.colliderect(mesh.rect):
			mesh_collision.append(mesh)
			collision_left = True
		if player.rect_right.colliderect(mesh.rect):
			mesh_collision.append(mesh)
			collision_right = True

	# Interaction player/objects
	waiting_user = None
	for mesh in maps.liste_interact:
		waiting_user = None
		
		# Custom mask interact
		try:
			if player.hitbox.colliderect(mesh.rect_interact):
				waiting_user = mesh
				break

		# Standard collision mask
		except AttributeError:
			if player.hitbox.colliderect(mesh.rect):
				waiting_user = mesh
				break

	# Borders map collision
	mesh_border_collision = []
	border_collision = False
	for borders in maps.list_collision_border:
		if player.rect_up.colliderect(borders):
			collision_up = True
			border_collision = True
		if player.rect_down.colliderect(borders):
			collision_down = True
			border_collision = True
		if player.rect_left.colliderect(borders):
			collision_left = True
			border_collision = True
		if player.rect_right.colliderect(borders):
			collision_right = True
			border_collision = True

		if border_collision == True:
			mesh_border_collision.append(borders)

	# Organization of the map by the 'z' layer
	organize_map(maps)

	# Move map reset
	x,y = 0,0

	# Controller pressed
	try:
		axes = joystick.get_numaxes()
		for i in range(axes):
			axis = joystick.get_axis(i)
			
			if i == 0:
				x_axis_left = axis
			elif i == 1:
				y_axis_left = axis

			elif i == 2:
				x_axis_right = axis
			elif i == 3:
				y_axis_right = axis

		# Left stick
		if x_axis_left < -float(os.environ['CONTROLLER_MARGE_STICK_LEFT']):
			left_stick = True
		else:
			left_stick = False

		if x_axis_left > float(os.environ['CONTROLLER_MARGE_STICK_LEFT']):
			right_stick = True
		else:
			right_stick = False

		if y_axis_left < -float(os.environ['CONTROLLER_MARGE_STICK_LEFT']):
			up_stick = True
		else:
			up_stick = False

		if y_axis_left > float(os.environ['CONTROLLER_MARGE_STICK_LEFT']):
			down_stick = True
		else:
			down_stick = False
		
		# Right stick
		if x_axis_right < -float(os.environ['CONTROLLER_MARGE_STICK_RIGHT']):
			left_stick_right = True
		else:
			left_stick_right = False

		if x_axis_right > float(os.environ['CONTROLLER_MARGE_STICK_RIGHT']):
			right_stick_right = True
		else:
			right_stick_right = False

		if y_axis_right < -float(os.environ['CONTROLLER_MARGE_STICK_RIGHT']):
			up_stick_right = True
		else:
			up_stick_right = False

		if y_axis_right > float(os.environ['CONTROLLER_MARGE_STICK_RIGHT']):
			down_stick_right = True
		else:
			down_stick_right = False
		
	# No joystick plug
	except:
		left_stick = False
		right_stick = False
		up_stick = False
		down_stick = False

		left_stick_right = False
		right_stick_right = False
		up_stick_right = False
		down_stick_right = False

		# Reload for reconnection...
		fps_count_joystick_reload += float(os.environ['DELTA_TIME'])
		if fps_count_joystick_reload == 1:
			joystick = load_joystick()
			fps_count_joystick_reload = 0

	# Player move
	if enable_move == True:
		# View control with right controller stick
		if up_stick_right:
			direction = 'up_collision'
		elif down_stick_right:
			direction = 'down_collision'
		elif left_stick_right:
			direction = 'left_collision'
		elif right_stick_right:
			direction = 'right_collision'

		# Diagonals
		if (Keys[convert_pygame_key(os.environ['KEYBOARD_UP'])] and Keys[convert_pygame_key(os.environ['KEYBOARD_LEFT'])]) or (up_stick and left_stick):
			if collision_left == False and collision_up == False:
				direction = 'left'
				x = player.speed_diagonal
				y = player.speed_diagonal
				player.fake_xy = (player.fake_xy[0]-player.speed_diagonal, player.fake_xy[1]-(0--y))
			else:
				direction = 'left_collision'

		elif (Keys[convert_pygame_key(os.environ['KEYBOARD_UP'])] and Keys[convert_pygame_key(os.environ['KEYBOARD_RIGHT'])]) or (up_stick and right_stick):
			if collision_right == False and collision_up == False:
				direction = 'right'
				x = -1*player.speed_diagonal
				y = player.speed_diagonal
				player.fake_xy = (player.fake_xy[0]+-x, player.fake_xy[1]-(0--y))
			else:
				direction = 'right_collision'

		elif (Keys[convert_pygame_key(os.environ['KEYBOARD_DOWN'])] and Keys[convert_pygame_key(os.environ['KEYBOARD_LEFT'])]) or (down_stick and left_stick):
			if collision_down == False and collision_left == False:
				direction = 'left'
				x = player.speed_diagonal
				y = -1*player.speed_diagonal
				player.fake_xy = (player.fake_xy[0]-player.speed_diagonal, player.fake_xy[1]+-y)
			else:
				direction = 'left_collision'

		elif (Keys[convert_pygame_key(os.environ['KEYBOARD_DOWN'])] and Keys[convert_pygame_key(os.environ['KEYBOARD_RIGHT'])]) or (down_stick and right_stick):
			if collision_down == False and collision_right == False:
				direction = 'right'
				x = -1*player.speed_diagonal
				y = -1*player.speed_diagonal
				player.fake_xy = (player.fake_xy[0]+-x, player.fake_xy[1]+-y)
			else:
				direction = 'right_collision'

		# Axes
		if Keys[convert_pygame_key(os.environ['KEYBOARD_LEFT'])] or left_stick:
			if collision_left == False:
				direction = 'left'
				x = player.speed
				player.fake_xy = (player.fake_xy[0]-player.speed, player.fake_xy[1])
			else:
				direction = 'left_collision'

		elif Keys[convert_pygame_key(os.environ['KEYBOARD_RIGHT'])] or right_stick:
			if collision_right == False:
				direction = 'right'
				x = -1*player.speed
				player.fake_xy = (player.fake_xy[0]+-x, player.fake_xy[1])
			else:
				direction = 'right_collision'

		elif Keys[convert_pygame_key(os.environ['KEYBOARD_UP'])] or up_stick:
			if collision_up == False:
				direction = 'up'
				y = player.speed
				player.fake_xy = (player.fake_xy[0], player.fake_xy[1]-(0--y))
			else:
				direction = 'up_collision'

		elif Keys[convert_pygame_key(os.environ['KEYBOARD_DOWN'])] or down_stick:
			if collision_down == False:
				direction = 'down'
				y = -1*player.speed
				player.fake_xy = (player.fake_xy[0], player.fake_xy[1]+-y)
			else:
				direction = 'down_collision'

	# Delta time correction
	x, y = x*dt, y*dt

	# Display ground of the map
	maps.show(Keys, x, y)

	# Map editor
	if editor != 'not_init':
		editor.show(Keys, MouseEvent, pygame.mouse.get_pos(), x, y)

	# Show ground effect
	effect.show_ground_effect(x,y)

	# Display
	for mesh in maps.group_blit:
		# Calcul entities collision
		if mesh in maps.liste_movement and editor == 'not_init':
			entity_collision = False

			for objects in maps.group_collision:
				if mesh.rect.colliderect(objects.rect) and mesh.rect != objects.rect:
					entity_collision = True

			for borders in maps.list_collision_border:
				if mesh.rect.colliderect(borders):
					entity_collision = True

			if entity_collision == False:
				mesh.focus_point(player.xy, maps)
			else:
				mesh.focus_point(player.xy, maps, object_collision=True)

		# The mesh is the player
		if mesh.id == 'Player':
			try:
				mesh.show(direction=direction, Keys=Keys)
			except UnboundLocalError:
				# No player movement
				mesh.show(Keys=Keys)

		# Common object
		else:
			mesh.show(x, y)
	
	if waiting_user != None:
		if joystick != False:
			mesh_user_action = waiting_user.waiting_user_action(Keys, joystick)
		else:
			mesh_user_action = waiting_user.waiting_user_action(Keys, joystick_not_plug)

		if mesh_user_action == 'interaction' or mesh_user_action == 'interaction_dontremove':
			if mesh_user_action == 'interaction_dontremove':
				add_interact_object = waiting_user
			interact_action = True
			interact_object = waiting_user
			maps.liste_interact.remove(waiting_user)

		# HUD level display
		elif type(mesh_user_action) == tuple:
			key_request = mesh_user_action

	# Parallel animation
	if interact_action:
		entity_interaction = interact_object.interaction()

		if entity_interaction == 'delete':
			enable_move = True
			interact_action = False
			# Addition of interactive object (ex dialogue)
			if add_interact_object != None:
				maps.liste_interact.append(add_interact_object)
				add_interact_object = None

		elif entity_interaction == 'disable_move':
			# Block player movement during certain actions
			enable_move = False
			show_menu = False # Prevents menu opening to avoid displacement bugs

	# Effects animation
	effect.show()

	# Light and shadows support
	if night_mode == True:
		filter = pygame.surface.Surface(size)
		filter.fill(pygame.color.Color('grey'))

		for mesh_light in maps.group_light:
			filter.blit(light, mesh_light.xy_light)
			screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

	# HUD mesh action
	try:
		mesh_blit_hud.blit_hud_action()
	except NameError:
		pass

	# Show waiting key
	try:
		interaction_class.waiting_key(key_request[0], key_request[1])
	except UnboundLocalError:
		pass

	# Show HUD
	if x == 0 and y == 0:
		hud_class.show('down', editor)
	else:
		hud_class.show('up', editor)

	# Show Menu
	if Keys[convert_pygame_key(os.environ['KEYBOARD_INVENTORY'])] and fps_count_interact != 'disable_move':
		show_menu = True
		enable_move = False
	elif Keys[pygame.K_ESCAPE]:
		show_menu = False
		enable_move = True
	
	if show_menu == True:
		menu.show(Keys)

	# Take a screenshot of the game and save it in Screenshots/[name_file].png
	if Keys[pygame.K_F1]:
		rect_screenshot = pygame.Rect(0, 0, int(largeur), int(hauteur))
		screenshot = screen.subsurface(rect_screenshot)
		pygame.image.save(screenshot, f"C:/Users/{os.environ['USERNAME']}/Documents/{title}/Screenshot/{time.time()}.png")
		print('A screenshot was taken')

	# Dev tools
	if debug == True:
		# Reload map
		if Keys[pygame.K_F9]:
			map_load_control = True

		# Show Hitbox
		if Keys[pygame.K_F10]:
			for mesh in maps.group_collision:
				pygame.draw.rect(screen, 'red', mesh, 2)
				pygame.draw.circle(screen, 'black', mesh.xy, 2)

			for mesh in maps.liste_interact:
				try:
					pygame.draw.rect(screen, '#4CA111', mesh.rect_interact, 1)
				except AttributeError:
					pygame.draw.rect(screen, 'green', mesh.rect, 1)

			for rect in maps.list_collision_border:
				pygame.draw.rect(screen, 'black', rect, 2)

			pygame.draw.rect(screen, 'blue', player.rect_up, 1)
			pygame.draw.rect(screen, 'blue', player.rect_down, 1)
			pygame.draw.rect(screen, 'blue', player.rect_left, 1)
			pygame.draw.rect(screen, 'blue', player.rect_right, 1)
			pygame.draw.rect(screen, 'orange', player.hitbox, 1)

		# Show Dev mode
		fps_text = font_pixel.render(f'DEV MODE', 1, pygame.Color('red'))
		xy_fps_text = fps_text.get_size()
		screen.blit(fps_text, (2,20))

		# Show FPS
		fps_text = font_pixel.render(f'Fps: {int(fpsClock.get_fps())} - {fpsClock.get_rawtime()}ms', 1, pygame.Color(color_dev))
		screen.blit(fps_text, (2,20+xy_fps_text[1]))

		# Show player position
		player_position_txt = font_pixel.render(f'Camera center: {int(player.fake_xy[0])}, {int(player.fake_xy[1])}', 1, pygame.Color(color_dev))
		screen.blit(player_position_txt, (2,20+xy_fps_text[1]*2))

		# Show collision player objects memory storage
		if mesh_collision == [] and mesh_border_collision == []:
			player_collision_ojects_txt = font_pixel.render('No collision object', 1, pygame.Color(color_dev))
		else:
			list_mesh_id = []
			for mesh in mesh_collision:
				list_mesh_id.append(mesh.id)

			for border in mesh_border_collision:
				list_mesh_id.append('border')

			player_collision_ojects_txt = font_pixel.render(f'Mesh(s) ID: {list_mesh_id}', 1, pygame.Color(color_dev))
			
		screen.blit(player_collision_ojects_txt, (2,20+xy_fps_text[1]*3))

		# Show used memory percent and memory free
		used_memory = font_pixel.render(
			f'Memory used: {int(psutil.virtual_memory().percent)}%', 1, pygame.Color(color_dev))
		screen.blit(used_memory, (2,20+xy_fps_text[1]*4))

		# Show used processor
		if fps_count_proc >= 0.25:
			proc_used = int(psutil.cpu_percent())
			fps_count_proc = 0
		else:
			fps_count_proc += dt

		used_processor = font_pixel.render(
			f'Processor used: {proc_used}%', 1, pygame.Color(color_dev))
		screen.blit(used_processor, (2,20+xy_fps_text[1]*5))

		# Show keyboard shortcut
		shortcut_keyboard = font_pixel.render('Shortcut: F9.reload F10.hitbox F11.log', 1, pygame.Color(color_dev))
		screen.blit(shortcut_keyboard, (2,20+xy_fps_text[1]*6))

	# HUD map editor
	if editor != 'not_init':
		editor.show_hud(maps.group_blit)

	# Mouse gestion
	if debug == True:
		# Show x,y mouse
		text_mouse_co = font_pixel.render(f'Mouse: {x_mouse}, {y_mouse}', 1, pygame.Color(color_dev))
		screen.blit(text_mouse_co, (2,20+xy_fps_text[1]*7))

	# Cancel action click widgets
	try:
		if left_clic == True:
			ancien_mesh_clic.no_clic_mouse()
			ancien_mesh_clic = None
	except AttributeError:
		pass

	# Mesh
	for mesh in maps.group_blit:
		clic = None
		if mesh.id != 'Player':
			collision_mouse = mesh.rect.collidepoint(x_mouse, y_mouse)

			if collision_mouse:
				if left_clic == True:
					clic = 'left'
				elif middle_clic == True:
					clic = 'middle'
				elif right_clic == True:
					clic = 'right'

				try:
					mesh.clic_mouse(clic)
				except AttributeError:
					pass

	# Collision
	for widget in widgets_class.list_widgets:
		clic = None
		collision_mouse = widget.rect.collidepoint(x_mouse, y_mouse)

		if collision_mouse:
			if left_clic == True:
				clic = 'left'
			elif middle_clic == True:
				clic = 'middle'
			elif right_clic == True:
				clic = 'right'

			try:
				widget.clic_mouse(clic)
				ancien_mesh_clic = widget
			except AttributeError:
				pass

# Game execution time measurement
start_time = time.time()

# Shutdown game function
def quit_game():
	global save_class
	time_played = int(time.time() - start_time) # In seconds
	print(f'time played: {time_played}s')

	save_class.list_save[1][1] = int(save_class.list_save[1][1]) + time_played
	save_class.save()

	pygame.joystick.quit()
	pygame.quit()
	sys.exit()

# Main loop
last_time = time.time()
pygame.event.set_allowed([QUIT, DROPFILE])
while True:
	# Delta time
	dt = time.time() - last_time
	last_time = time.time()
	os.environ['DELTA_TIME'] = str(dt)

	# Fill refresh
	screen.fill('black')

	# System events
	MouseEvent = []
	for event in pygame.event.get():

		if event.type == QUIT:
			quit_game()

		elif event.type == DROPFILE:
			validation_code = interaction_class.drop_file(event.file)
			if validation_code != False:
				print(validation_code)

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			MouseEvent.append('LEFTCLIC')

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
			MouseEvent.append('MOLETTECLIC')

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			MouseEvent.append('RIGHTCLIC')

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			MouseEvent.append('SCROLLUP')

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
			MouseEvent.append('SCROLLDOWN')

	# User events
	Keys = pygame.key.get_pressed()

	# Map loading
	if map_load_control:
		infos_map = load_map(save_class.list_save[1][0], save_class)
		
		try:
			maps, effect, editor = infos_map
		except ValueError:
			maps, effect, editor = infos_map[0], infos_map[1], 'not_init'

		map_load_control = False

	# Refresh and calculations
	if update_loop:
		update(Keys, MouseEvent)

	# Display main menu of the game
	if show_main_menu:
		# Dev variables
		logging.debug('Game loop starting...')
		update_loop = True
		show_main_menu = False

		if main_menu.show(x_mouse, y_mouse) == 'launch_game':
			update_loop = True
			show_main_menu = False

	# Mouse gestion
	left_clic, middle_clic, right_clic = pygame.mouse.get_pressed()
	x_mouse, y_mouse = pygame.mouse.get_pos()

	if x_mouse not in (0, size[0]) and y_mouse not in (0, size[1]):
		if pygame.mouse.get_pressed()[0]:
			screen.blit(image_cursor_click, (x_mouse, y_mouse))
		else:
			screen.blit(image_cursor, (x_mouse, y_mouse))

	# Show the logo when the game starting
	try:
		if show_logo:
			if logo_class.show() == 'end_logo':
				show_main_menu = True
				show_logo = False
	except NameError:
		pass

	if hardware_acceleration:
		# Prepare to render the texture-mapped window
		glClear(GL_COLOR_BUFFER_BIT)
		glLoadIdentity()
		glDisable(GL_LIGHTING)
		glEnable(GL_TEXTURE_2D)

		# Draw texture OpenGL Texture
		surfaceToTexture(screen)
		glBindTexture(GL_TEXTURE_2D, texID)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0); glVertex2f(-1, 1)
		glTexCoord2f(0, 1); glVertex2f(-1, -1)
		glTexCoord2f(1, 1); glVertex2f(1, -1)
		glTexCoord2f(1, 0); glVertex2f(1, 1)
		glEnd()

	# Show window after 1 frame for hide pygame init
	if screen_hidden:
		if flags != None:
			screen = pygame.display.set_mode(size, flags | pygame.SHOWN, vsync=vsync)
		else:
			screen = pygame.display.set_mode(size, pygame.SHOWN, vsync=vsync)
		logging.debug('Show game window')

		if show_logo:
			logo_class = Logo(screen, size, interaction_class)

		screen_hidden = False

	# Update ticks per second
	fpsClock.tick(int(fps_lock))

	# Flip/Update the entire screen
	if hardware_acceleration:
		pygame.display.flip()
	else:
		pygame.display.update()