import os, sys

# Console arguments
for arg in sys.argv[1:]:
	print(arg)

# Informations
os.environ['GAME_TITLE'] = 'GameEngineByLiyonDevCanal'
os.environ['GAME_VERSION'] = 'DevBuild n°NoIdea'
os
# Set environment variables - 0=False ; 1=True -> str
os.environ['DEVMODE'] = '1'
os.environ['EDITOR'] = '0'
os.environ['SHOW_LOGO'] = '1'
os.environ['FPS'] = '500'

# Launch engine and game
from engine import *