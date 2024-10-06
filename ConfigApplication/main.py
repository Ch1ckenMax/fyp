from src.stlink_interface import VCUInterface
from src.config_reader import ConfigReader
from src.gui import GUI

# Constants
CONFIG_PATH = ".\\config\\config.json"
ST_LINK_EXE_PATH = ".\\externlib\\stlink-1.7.0-x86_64-w64-mingw32\\bin\\"
MEMORY_SIZE = 0x20000

vcuInterface = VCUInterface(ST_LINK_EXE_PATH, MEMORY_SIZE)
configReader = ConfigReader(CONFIG_PATH)

gui = GUI(configReader, vcuInterface)
gui.initElements()
gui.startGUILoop()

# Load Config

# Create a GUI

# Check if ST-LINK exists in the env var