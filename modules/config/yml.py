from os import getenv
from confuse import Configuration

CONFIG = Configuration('DiscordBot', __name__)
CONFIG.set_file(getenv('CONFIG_PATH'))