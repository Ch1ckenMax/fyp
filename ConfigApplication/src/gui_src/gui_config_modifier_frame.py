from tkinter import messagebox
import customtkinter

from src.gui_src.gui_config_form import ConfigFormFrame
from src.gui_src.gui_config_button_vcu import ConfigVCUButtonFrame
from src.gui_src.gui_config_form_control import ConfigFormControlFrame

CONFIG_FORM_HEIGHT = 700

class ConfigModifierFrame(customtkinter.CTkFrame):
    def __init__(self, parent, 
                configReader,
                stlinkInterface, write_flash_memory_address):
        super().__init__(parent)

        self.write_flash_memory_address = write_flash_memory_address

        # Configure the frame
        self.grid_columnconfigure(0, weight = 90)
        self.grid_columnconfigure(1, weight = 5)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 99)

        # Dummy frame placeholder to be replaced when the config is loaded
        self.config_form = customtkinter.CTkTextbox(self, height = CONFIG_FORM_HEIGHT)
        self.config_form.insert("0.0", "Plase click \"Load Default Config\" on the right to start modifying the config.")
        self.config_form.configure(state = "disabled")
        self.config_form.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = 5, sticky = "news")

        # VCU Button Frame
        self.config_vcu_button = ConfigVCUButtonFrame(self)
        self.config_vcu_button.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "new")
        self.config_vcu_button.disableWriteToFlashButton()

        # Config Form Control Frame
        self.config_form_control = ConfigFormControlFrame(self)
        self.config_form_control.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = "news")
        self.config_form_control.disableSaveConfigButton()
        
        # Configure the variables
        self.configReader = configReader
        self.stlinkInterface = stlinkInterface
        self.configDict = None
        self.configFormLoaded = False

    def onConfigFormLoaded(self, configDict):
        # Update states
        self.configDict = configDict
        self.configFormLoaded = True

        # Remove the current form widget and replace with a new one
        self.config_form.destroy()
        self.config_form = ConfigFormFrame(self, configDict, label_text = "Config Form", height = CONFIG_FORM_HEIGHT)
        self.config_form.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = 5, sticky = "news")

        # Enable the write to flash and save to config button
        self.config_vcu_button.enableWriteToFlashButton()
        self.config_form_control.enableSaveConfigButton()

