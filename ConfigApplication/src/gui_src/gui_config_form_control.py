from tkinter import messagebox
import customtkinter

BUTTON_WIDTH = 200

class ConfigFormControlFrame(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 40)
        self.grid_columnconfigure(0, weight = 1)

        # Title
        self.title = customtkinter.CTkLabel(self, text = "Form Control Pane", bg_color = "grey25")
        self.title.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "new")

        # Button for loading default config
        self.load_config_button = customtkinter.CTkButton(self, text="Load Default Config", command=self.__loadConfigUIFunc, width = BUTTON_WIDTH)
        self.load_config_button.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "new")
    
    def __loadConfigUIFunc(self):
        (result, errorMessage) = self.parent.configReader.readConfigFile()

        # If the config is already loaded, warn the user that this will overwrite the current form
        if self.parent.configFormLoaded:
            answer = messagebox.askquestion("Overwriting Current Config", "Are you sure you would like to load the config? \n Unsaved changes WILL be discarded.")
            if answer != "yes":
                return

        if result is None:
            messagebox.showinfo(title = "Load from Default Config", message = "Cannot load the default config. Please make sure that a correct config is placed in the path: " + self.configReader.configPath + ". Error Info: " + errorMessage)
            return
        messagebox.showinfo(title = "Load from Default Config", message = "Load Default Config was successful!")
        self.parent.onConfigFormLoaded(result)
        