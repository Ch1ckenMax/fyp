import tkinter as tk
from tkinter import messagebox
import customtkinter

class GUI:
    def __init__(self,
                configReader,
                stlinkInterface):
        # Configure the root
        customtkinter.set_appearance_mode("dark")
        self.root = customtkinter.CTk()
        self.root.title("HKU Racing VCU Config Modifier")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Configure the tabs
        tabview = customtkinter.CTkTabview(master = self.root)
        tabview.pack(fill = "both", expand = True)

        self.configModifierTab = tabview.add("Config Modifier")
        self.calibratorTab = tabview.add("Calibrator")
        tabview._segmented_button.grid(sticky="W")

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
        else:
            messagebox.showinfo(title = "Config Read", message = "Config read was successful! Config: " + str(result))
            self.configDict = result

    def __writeToFlashUIFunc(self):
        (result, errorMessage) = self.stlinkInterface.WriteToFlash(str(self.configDict), 0x8010000, ".\\tempbuf.bin")

        if result:
            messagebox.showinfo(title = "Write to Flash", message = "Write Success!")
        else:
            messagebox.showinfo(title = "Write to Flash", message = "Write Failed. Error Info: " + errorMessage)


    def initElements(self): 
        # Button for checking connection
        hasConnectionButton = customtkinter.CTkButton(self.configModifierTab, text="Check connection to STM32 board", command=self.__hasConnectionUIFunc)
        hasConnectionButton.grid(row = 0, column = 1, pady = 10)
        
        # Button for reading config
        readConfigButton = customtkinter.CTkButton(self.configModifierTab, text="Read Config", command=self.__readConfigUIFunc)
        readConfigButton.grid(row = 1, column = 1, pady = 10)

        writeToFlashButton = customtkinter.CTkButton(self.configModifierTab, text="Write to Flash", command=self.__writeToFlashUIFunc)
        writeToFlashButton.grid(row = 2, column = 1, pady = 10)
    
    def startGUILoop(self):
        self.root.mainloop()