import os, shutil, configparser, pickle

class Save():
	def __init__(self, title, language, nb_save:int):
		# Find the save path
		self.name_user = os.environ['USERNAME']
		self.path_save = f'C:/Users/{self.name_user}/Documents/{title}/Saves/{str(nb_save)}/'
		self.path_directory = f'C:/Users/{self.name_user}/Documents/{title}'

		# Game language
		self.language = language

	def path(self):
		return self.path_save

	def current_language(self):
		return self.language

	def check_save_folder(self):
		try:
			# Check if the save folder is on the machine
			open(f'{self.path_save}game_data.plk', 'r')

		except FileNotFoundError:
			# Copy clean directory
			generate_new_save(self.path_directory)

	def load_language(self, name_file):
		# Load dialogue lines for a character with his id
		with open('Content/Languages/' + self.language + '/' + name_file + '.dll') as content_language:
			language_content = content_language.read().splitlines()

		return language_content

	def load(self):
		# Load every data of the game except language
		self.list_save = []

		with open(f'{self.path_save}game_data.plk', 'rb') as file_game_data:
			self.list_save = pickle.load(file_game_data)

		return self.list_save

	def save(self):
		# Save all game data
		with open(f'{self.path_save}game_data.plk', 'wb') as file_game_data:
			pickle.dump(self.list_save, file_game_data, pickle.HIGHEST_PROTOCOL)

	def transaction_money(self, mode, nb_money):
		if mode == '+':
			self.list_save[0][10] = int(self.list_save[0][10]) + nb_money
		elif mode == '-':
			self.list_save[0][10] = int(self.list_save[0][10]) - nb_money

'''
STRUCTURE SAVE FILES

[0] PLAYER
0: Name
1: Sex
2: Hairs
3: Eyes
4: Body
5: Leg
6: Foot
7: Skin
8: Weapon
9: Side action
10: Money
11: Level

[1] WORLD
0: Current map
1: Time played in seconds
2: Day
3: Month
4: Years
5: Weather
6: Hours
7: World Effect like rain

[2] QUESTS
1: Title quest
2: Dictionnary with every tasks for the selected quest
3;-1: List with all unlock quests not tracked

[3] ID_DIALOG.DLL
0;-1: Character ID dialogue level

[4] INVENTORY.DLL
0;-1: Player items and objects

'''

def generate_new_save(path_directory):
	save_player = [
	'Player',
	'h',
	10,
	12,
	10,
	10,
	10,
	10,
	10,
	'steal',
	100,
	1
	]

	save_world = [
	0,
	0,
	1,
	'Month',
	100,
	'weather_clear',
	'6:00',
	'None'
	]

	save_quests = [
	'FINIR LE DEVELOPPEMENT DU JEU',
	{'Corriger tous les bugs': True, 'Trouver un truc original': False},
	[]
	]

	save_id_dialog = [
	0,
	0
	]

	save_inventory = [
	]

	new_save = [
	save_player,
	save_world,
	save_quests,
	save_id_dialog,
	save_inventory]

	os.mkdir(f'{path_directory}', 0o666)
	os.mkdir(f'{path_directory}/Saves', 0o666)
	os.mkdir(f'{path_directory}/Saves/0', 0o666)
	with open(f'{path_directory}/Saves/0/game_data.plk', 'wb') as file_game_data:
		pickle.dump(new_save, file_game_data, pickle.HIGHEST_PROTOCOL)