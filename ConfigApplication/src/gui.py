import tkinter as tk
from tkinter import messagebox

class GUI:
    def __init__(self,
                configReader,
                stlinkInterface):
        # Configure the root
        self.root = tk.Tk()
        self.root.title("HKU Racing VCU Config Modifier")
        self.root.geometry("800x600")
        self.root.configure(background = "grey")

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

    def initElements(self): 
        # Button for checking connection
        hasConnectionButton = tk.Button(self.root, text="Check connection to STM32 board", command=self.__hasConnectionUIFunc)
        hasConnectionButton.pack(pady = 10)

        # Button for reading config
        readConfigButton = tk.Button(self.root, text="Read Config", command=self.__readConfigUIFunc)
        readConfigButton.pack(pady = 10)
    
    def startGUILoop(self):
        self.root.mainloop()