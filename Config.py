
import os
import sys

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

FONTS_DIR = os.path.join(PROJECT_DIR, 'Gui', 'Fonts')
TEXTURES_DIR = os.path.join(PROJECT_DIR, 'Gui', 'Textures')

LOG_LVL = 'CRITICAL'
LOG_FILE = None
LOG_FMT = '%(asctime)s %(levelname)s %(message)s'

MCAST_GRP = '239.192.0.4'
MCAST_PORT = 9192
MCAST_TTL = 1

GAME_CONFIG_FILE = 'GameConfig.txt'
