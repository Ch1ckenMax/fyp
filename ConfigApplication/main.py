from src.stlink_interface import VCUInterface
from src.config_reader import ConfigReader
from src.gui import GUI

# Constants
CONFIG_PATH = ".\\config\\config.json"
ST_LINK_EXE_PATH = ".\\externlib\\stlink-1.7.0-x86_64-w64-mingw32\\bin\\"
TEMP_BUFFER_PATH = ".\\tempbuf.bin"
MEMORY_SIZE = 0x10000
MEMORY_START_ADDRESS = 0x8010000

vcuInterface = VCUInterface(ST_LINK_EXE_PATH, MEMORY_SIZE, MEMORY_START_ADDRESS)
configReader = ConfigReader(CONFIG_PATH)

content = "what is the buffer of this? ASSHOLE!"
# print(vcuInterface.WriteToFlash(content, MEMORY_START_ADDRESS + 0x400, TEMP_BUFFER_PATH))

gui = GUI(configReader, vcuInterface)
gui.initElements()
gui.startGUILoop()

# Load Config

# Create a GUI

# Check if ST-LINK exists in the env var