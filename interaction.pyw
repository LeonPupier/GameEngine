import pygame, keyboard, os, configparser

pygame.font.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

# Engine configuration fo volume level
config_engine = configparser.ConfigParser()
config_engine.read('Content/engine.ini')
volume = float(config_engine['CONFIG']['Volume'])

def convert_pygame_key(key):
	list_user_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	list_pygame_key = [
					  pygame.K_a,
					  pygame.K_b,
					  pygame.K_c,
					  pygame.K_d,
					  pygame.K_e,
					  pygame.K_f,
					  pygame.K_g,
					  pygame.K_h,
					  pygame.K_i,
					  pygame.K_j,
					  pygame.K_k,
					  pygame.K_l,
					  pygame.K_m,
					  pygame.K_n,
					  pygame.K_o,
					  pygame.K_p,
					  pygame.K_q,
					  pygame.K_r,
					  pygame.K_s,
					  pygame.K_t,
					  pygame.K_u,
					  pygame.K_v,
					  pygame.K_w,
					  pygame.K_x,
					  pygame.K_y,
					  pygame.K_z]

	if key in list_user_key:
		return list_pygame_key[list_user_key.index(key)]
	return pygame.K_e

def move_map(screen, rect, x, y, xy):
	xy = (xy[0]+x, xy[1]+y)
	rect.x, rect.y = xy[0], xy[1]
	return xy, rect, rect.x, rect.y


def organize_map(maps):
	list_blit = maps.group_blit.copy()
	coordonnee = []
	list_blit_organize = []

	for mesh in list_blit:
		coordonnee.append(mesh.xy[1]+mesh.resize[1])

	while coordonnee != []:
		value_min = min(coordonnee)

		index_min = coordonnee.index(value_min)
		list_blit_organize.append(list_blit[index_min])

		list_blit.pop(index_min)
		coordonnee.remove(value_min)

	maps.group_blit = list_blit_organize


class Interaction():
	def __init__(self, screen, size):
		self.screen = screen
		self.size = size

		self.image_dialog_box = pygame.image.load('Content/Ui/dialog/box.png').convert_alpha()
		self.size_dialog_box = self.image_dialog_box.get_size()

		self.image_dialog_box_up = pygame.image.load('Content/Ui/dialog/box_up.png').convert_alpha()
		size_dialog_box_up = self.image_dialog_box_up.get_size()
		self.resize_dialog_up = (int((size[0]*size_dialog_box_up[0]*6)/1920), int((size[1]*size_dialog_box_up[1]*6)/1080))
		self.image_dialog_box_up = pygame.transform.scale(self.image_dialog_box_up, self.resize_dialog_up)

		self.image_dialog_box_down = pygame.image.load('Content/Ui/dialog/box_down.png').convert_alpha()
		size_dialog_box_down = self.image_dialog_box_down.get_size()
		self.resize_dialog_down = (int((size[0]*size_dialog_box_down[0]*6)/1920), int((size[1]*size_dialog_box_down[1]*6)/1080))
		self.image_dialog_box_down = pygame.transform.scale(self.image_dialog_box_down, self.resize_dialog_down)

		# Bubble info
		self.time_animation_infos = 0
		self.slide_infos = 0.33
		self.slide_strength = 0.2
		self.animation_infos = 0

		self.resize_position_player = (int((size[0]*96)/1920), int((size[1]*132)/1080))
		self.resize_letter = (int((size[0]*32)/1920), int((size[1]*32)/1080))

		# Center
		self.image_infos_bulle = pygame.image.load('Content/Ui/keys/11.png').convert_alpha()
		self.size_infos_bulle = self.image_infos_bulle.get_size()

		# Left corner
		self.image_left_bord_infos_bulle = pygame.image.load('Content/Ui/keys/10.png').convert_alpha()
		size_bord_infos_bulle = self.image_left_bord_infos_bulle.get_size()
		self.resize_bords_infos_bulle = (int((size[0]*size_bord_infos_bulle[0]*6)/1920), int((size[1]*size_bord_infos_bulle[1]*6)/1080))
		self.image_left_bord_infos_bulle = pygame.transform.scale(self.image_left_bord_infos_bulle, self.resize_bords_infos_bulle)

		# Right corner
		self.image_right_bord_infos_bulle = pygame.image.load('Content/Ui/keys/12.png').convert_alpha()
		self.image_right_bord_infos_bulle = pygame.transform.scale(self.image_right_bord_infos_bulle, self.resize_bords_infos_bulle)

		self.xy_info_letter = ((size[0]/2-self.resize_position_player[0]/1.1, size[1]/2-self.resize_position_player[1]))

		# Dialogue music
		self.sound_dialog = pygame.mixer.Sound('Content/Sounds/text_typing.wav')

		# Dialog
		self.size_line = 70
		self.text = []
		self.index_text = 0
		self.nb_line = 0
		self.majuscule_control = False
		self.waiting_upper_control = False
		self.fps_dialog = 0
		self.time_dialog = 2
		self.color_dialog = '#3C3C3C'
		self.size_font = int((size[0]*25)/1600)
		self.size_font_bubble_info = int((size[0]*24/1600))
		self.size_font_dialog = int((size[0]*28)/1600)
		self.font = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font)
		self.font_dialog = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font_dialog)
		self.size_text = self.font_dialog.render('TEXT', self.size_font, pygame.Color(self.color_dialog)).get_size()
		self.font_lettre = pygame.font.Font("Content/Fonts/pixel_game.ttf", self.size_font_bubble_info)
		self.size_lettre = self.font_lettre.render('X', self.size_font_bubble_info, pygame.Color(self.color_dialog)).get_size()


	def play_sound(self, sound, volume_sound=None, nb_play=None):
		self.sound = 'Content/Sounds/' + sound + '.wav'
		try:
			load_sound = pygame.mixer.Sound(self.sound)
		except:
			return 'sound_not_exist'

		if nb_play != None:
			load_sound.play(nb_play)
		else:
			load_sound.play()

		# Global volume
		if volume_sound != None:
			load_sound.set_volume(volume_sound)
		else:
			load_sound.set_volume(volume)

	def waiting_key(self, key, txt):
		dt = float(os.environ['DELTA_TIME'])

		# Centered dynamic display
		interact_text = self.font_lettre.render(txt, 1, 'black')
		size_text_bubble_info = interact_text.get_size()
		
		self.image_letter = pygame.image.load(f'Content/Ui/keys/{key}.png').convert_alpha()
		self.image_letter = pygame.transform.scale(self.image_letter, self.resize_letter)

		# Animation of the interaction tooltip
		self.time_animation_infos += dt

		if self.time_animation_infos <= self.slide_infos:
			self.animation_infos += self.slide_strength
		elif self.slide_infos < self.time_animation_infos <= self.slide_infos*2:
			self.animation_infos -= self.slide_strength
		else:
			self.time_animation_infos = 0
			self.animation_infos = 0

		self.resize_infos_bulle = (size_text_bubble_info[0], int((self.size[1]*self.size_infos_bulle[1]*6)/1080))
		self.image_infos_bulle = pygame.transform.scale(self.image_infos_bulle, self.resize_infos_bulle)
		self.xy_info_bulle = (self.size[0]/2-self.resize_infos_bulle[0]/2, self.size[1]/2-self.resize_position_player[1]/1.1)

		self.screen.blit(self.image_infos_bulle, (self.xy_info_bulle[0], self.xy_info_bulle[1]+self.animation_infos))
		self.screen.blit(self.image_left_bord_infos_bulle, (self.xy_info_bulle[0]-self.resize_bords_infos_bulle[0], self.xy_info_bulle[1]+self.animation_infos))
		self.screen.blit(self.image_right_bord_infos_bulle, (self.xy_info_bulle[0]+self.resize_infos_bulle[0], self.xy_info_bulle[1]+self.animation_infos))

		self.xy_text_info_bulle = (self.size[0]/2-size_text_bubble_info[0]/2, self.size[1]/2-self.resize_position_player[1]/1.13)
		self.screen.blit(interact_text, (self.xy_text_info_bulle[0], self.xy_text_info_bulle[1]+self.animation_infos))

		self.screen.blit(self.image_letter, (self.xy_info_bulle[0]-self.resize_bords_infos_bulle[0]*2, self.xy_info_letter[1]+self.animation_infos))

	def dialog(self, pnj_txt, id_dialog):
		# Line break if string protrudes from dialog
		list_line = []
		start_split_line = 0
		end_split_line = 1

		while True:
			line = pnj_txt[start_split_line : self.size_line*end_split_line]
			if line != '':
				list_line.append(line)
				start_split_line = self.size_line*end_split_line
				end_split_line += 1
			else:
				break

		# Reorganization line back words too long
		try:
			for nb_sentence in range(len(list_line)):
				if list_line[nb_sentence+1][0] != ' ':
					list_line[nb_sentence+1] = list_line[nb_sentence].split(' ')[-1] + list_line[nb_sentence+1]
					line_reorganisation = list_line[nb_sentence].split(' ')
					del line_reorganisation[-1]
					list_line[nb_sentence] = ' '.join(line_reorganisation)
		except IndexError:
			pass # Line too short

		# Remove unnecessary space from beginning of line
		for nb_sentence in range(len(list_line)):
			try:
				if list_line[nb_sentence][0] == ' ':
					line_reorganisation = list_line[nb_sentence].split(' ')
					del line_reorganisation[0]
					list_line[nb_sentence] = ' '.join(line_reorganisation)
			except IndexError:
				pass # Sentence too short

		# Dialog box
		self.resize_dialog = (int((self.size[0]*self.size_dialog_box[0]*6)/1920), int((self.size[1]*self.size_text[1]*1.3*len(list_line))/1080))
		self.image_dialog_box = pygame.transform.scale(self.image_dialog_box, self.resize_dialog)
		self.position_dialog = (self.size[0]/2-self.resize_dialog[0]/2, self.size[1]-self.resize_dialog[1]-self.resize_dialog_down[1]*1.5)
		
		self.position_dialog_up = (self.position_dialog[0], self.position_dialog[1]-self.resize_dialog_up[1])
		self.position_dialog_down = (self.position_dialog[0], self.position_dialog[1]+self.resize_dialog[1])

		self.screen.blit(self.image_dialog_box, self.position_dialog)
		self.screen.blit(self.image_dialog_box_up, self.position_dialog_up)
		self.screen.blit(self.image_dialog_box_down, self.position_dialog_down)

		try:
			self.position_text = (self.position_dialog[0]+(self.resize_dialog[0]/20), self.position_dialog[1])

			# Display animated preceding lines
			if self.nb_line != 0:
				for line_complete in range(self.nb_line):
					fps_text = self.font_dialog.render(list_line[line_complete], self.size_font, pygame.Color(self.color_dialog))
					self.screen.blit(fps_text, self.position_text)
					self.position_text = (self.position_text[0], self.position_text[1]+self.size_text[1])

			# Display the message dynamically
			if self.fps_dialog == self.time_dialog:
				self.text.append(list_line[self.nb_line][self.index_text])
				self.index_text += 1
				self.fps_dialog = 0
			else:
				self.fps_dialog += 1

			# The player wants to skip the message
			if pygame.key.get_pressed()[pygame.K_SPACE]:
				self.index_text = len(pnj_txt)+1

			fps_text = self.font_dialog.render(''.join(self.text), self.size_font, pygame.Color(self.color_dialog))

			# Play the typing sound
			self.sound_dialog.play()
			self.sound_dialog.set_volume(volume)

			self.screen.blit(fps_text, self.position_text)

			return id_dialog # Continue
		except IndexError:
			if self.nb_line != len(list_line): # Number of lines in the dialog
				fps_text = self.font_dialog.render(''.join(self.text), self.size_font, pygame.Color(self.color_dialog))
				self.screen.blit(fps_text, self.position_text)
				
				self.nb_line += 1
				self.text = []
				self.index_text = 0
				self.fps_dialog = 0

				return id_dialog # Next line
			else:
				# The message was broadcast in its entirety
				if pygame.key.get_pressed()[pygame.K_SPACE]:
					# Next dialogue
					self.text = []
					self.index_text = 0
					self.nb_line = 0
					self.fps_dialog = 0
					return id_dialog + 0.5
				else:
					return id_dialog

	def detect_keys(self, Keys):
		# Keyboard
		minuscule = 'abcdefghijklmnopqrstuvwxyz'
		nombres = '0123456789'

		if keyboard.is_pressed('backspace'):
			return 'backspace'
		elif keyboard.is_pressed('space'):
			return ' '

		if keyboard.is_pressed('caps_lock'):
			self.waiting_upper_control = True
			caps_lock_not_clicked = True
		else:
			caps_lock_not_clicked = False

		if self.waiting_upper_control and caps_lock_not_clicked == False:
			if self.majuscule_control:
				self.majuscule_control = False
			else:
				self.majuscule_control = True
			self.waiting_upper_control = False

		for lettre in minuscule:
			if keyboard.is_pressed(lettre):
				if self.majuscule_control:
					return lettre.upper()
				else:
					return lettre	

		for chiffre in nombres:
			if keyboard.is_pressed(chiffre):
				return chiffre

		return None

	def drop_file(self, file):
		try:
			file_code = open(file, 'r')
			code = file_code.read()
			file_code.close()

			list_code = ['$r4+tzz:U3-9lq0S{UG5GEDFylQ0oucgsz2IZ3G@bM{ggL6=2]%DV<]DJ3GCeBbh0)iV4^v14TCw`pi)Pf^^i{BTKcHAd{edhS']

			name = file.split("]")[-1].split('.')[0].split(' ')[0]

			if code in list_code:
				return name

			else:
				return False

		except:
			return False

'''
Fonction show standard

def show():
	self.old_position = self.xy
	self.xy, self.rect, self.rect.x, self.rect.y = move_map(self.screen, self.rect, x, y, self.xy)
	#self.screen.blit(self.images[self.idx], self.xy)
	self.screen.blit(self.image, self.xy)
'''

'''
DESCRIPTION CONTROLLER:

A Button        - Button 0
B Button        - Button 1
X Button        - Button 2
Y Button        - Button 3
Left Bumper     - Button 4
Right Bumper    - Button 5
Back Button     - Button 6
Start Button    - Button 7
L. Stick In     - Button 8
R. Stick In     - Button 9
Guide Button    - Button 10

'''