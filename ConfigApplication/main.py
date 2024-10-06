from src.stlink_interface import VCUInterface
from src.config_reader import ConfigReader

# Constants
CONFIG_PATH = ".\\config\\config.json"
ST_LINK_EXE_PATH = ".\\externlib\\stlink-1.7.0-x86_64-w64-mingw32\\bin\\"
MEMORY_SIZE = 0x20000


# Load Config

# Create a GUI

# Check if ST-LINK exists in the env var

configReader = ConfigReader()

print(configReader.readConfig(CONFIG_PATH))