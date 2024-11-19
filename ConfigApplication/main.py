from src.stlink_interface import VCUInterface
from src.config_reader import ConfigReader
from src.gui import GUI

# Constants
CONFIG_PATH = ".\\config\\config.json"
ST_LINK_EXE_PATH = ".\\externlib\\stlink-1.7.0-x86_64-w64-mingw32\\bin\\"
ST_PROGRAMMER_EXE = ".\\externlib\\STM32CubeProgrammer\\bin\\STM32_Programmer_CLI.exe"
RT_CONSOLE_EXE = ".\\externlib\\RTconsole.exe"
TEMP_BUFFER_PATH = ".\\tempbuf.bin"
MEMORY_SIZE = 0x10000
MEMORY_START_ADDRESS = 0x8010000
STM_SYS_CLOCK_MHZ = "64"

vcuInterface = VCUInterface(ST_LINK_EXE_PATH, ST_PROGRAMMER_EXE, RT_CONSOLE_EXE, MEMORY_SIZE, MEMORY_START_ADDRESS, STM_SYS_CLOCK_MHZ)
configReader = ConfigReader(CONFIG_PATH)

gui = GUI(configReader, vcuInterface, MEMORY_START_ADDRESS)
gui.startGUILoop()