from tkinter import messagebox
import customtkinter

from src.config_form_gui import ConfigFormFrame

class ConfigModifierFrame(customtkinter.CTkFrame):
    def __init__(self, parent, 
                configReader,
                stlinkInterface):
        super().__init__(parent)

        # Configuriating the frame
        self.grid_columnconfigure(0, weight=7)
        self.grid_columnconfigure(0, weight=3)

        # Dummy frame placeholder to be replaced when the config is loaded
        self.configForm = customtkinter.CTkLabel(self, text="Plase click \"Read Config\" on the right to start modifying the config.", fg_color="black")
        self.configForm.grid(row = 0, column = 0, rowspan = 3)

        # Button for checking connection
        hasConnectionButton = customtkinter.CTkButton(self, text="Check connection to STM32 board", command=self.__hasConnectionUIFunc)
        hasConnectionButton.grid(row = 0, column = 1, pady = 10)
        
        # Button for reading config
        readConfigButton = customtkinter.CTkButton(self, text="Read Config", command=self.__readConfigUIFunc)
        readConfigButton.grid(row = 1, column = 1, pady = 10)

        # Button for writing to flash of STM32
        writeToFlashButton = customtkinter.CTkButton(self, text="Write to Flash", command=self.__writeToFlashUIFunc)
        writeToFlashButton.grid(row = 2, column = 1, pady = 10)
        
        # Configure the variables
        self.configReader = configReader
        self.stlinkInterface = stlinkInterface
        self.configDict = None

    def __hasConnectionUIFunc(self):
        (result, errorMessage) = self.stlinkInterface.HasConnection()

        if result:
            messagebox.showinfo(title = "Connection", message = "There is connection with exactly one STM32 board.")
        else:
            messagebox.showinfo(title = "Connection", message = "STM32 board not found. Error Info: " + errorMessage)
    
    def __readConfigUIFunc(self):
        (result, errorMessage) = self.configReader.readConfigFile()

        if result is None:
            messagebox.showinfo(title = "Config Read", message = "Cannot read the config. Please make sure that a correct config is placed in the path: " + self.configReader.configPath + ". Error Info: " + errorMessage)
            return
        messagebox.showinfo(title = "Config Read", message = "Config read was successful! Config: " + str(result))
        self.configDict = result
        self.__ReplaceConfigForm(result)

    def __writeToFlashUIFunc(self):
        (result, errorMessage) = self.stlinkInterface.WriteToFlash(str(self.configDict), 0x8010000, ".\\tempbuf.bin")

        if result:
            messagebox.showinfo(title = "Write to Flash", message = "Write Success!")
        else:
            messagebox.showinfo(title = "Write to Flash", message = "Write Failed. Error Info: " + errorMessage)

    def __ReplaceConfigForm(self, configDict):
        # Remove the current form widget and replace with a new one
        self.configForm.destroy()
        self.configForm = ConfigFormFrame(self, configDict, fg_color="black")
        self.configForm.grid(row = 0, column = 0, rowspan = 3)

