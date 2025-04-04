from tkinter import messagebox, filedialog
import customtkinter
from customtkinter import ThemeManager
import json
from datetime import datetime

BUTTON_WIDTH = 200

class ConfigFormControlFrame(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 20)
        self.grid_rowconfigure(2, weight = 20)
        self.grid_rowconfigure(3, weight = 20)
        self.grid_columnconfigure(0, weight = 1)

        # Title
        self.title = customtkinter.CTkLabel(self, text = "Form Control Pane", bg_color = "grey25")
        self.title.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "new")

        # Button for loading default config
        self.load_default_config_button = customtkinter.CTkButton(self, text="Load Default Config", command=self.__loadDefaultConfigUIFunc, width = BUTTON_WIDTH)
        self.load_default_config_button.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "new")
        
        # Button for loading a user-defined config
        self.load_user_config_button = customtkinter.CTkButton(self, text="Load User Config", command=self.__loadUserConfigUIFunc, width = BUTTON_WIDTH)
        self.load_user_config_button.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "new")
        
        # Button for saving a user-defined config
        self.save_user_config_button = customtkinter.CTkButton(self, text="Save User Config", command=self.__saveUserConfigUIFunc, width = BUTTON_WIDTH)
        self.save_user_config_button.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "new")
    
    def __loadDefaultConfigUIFunc(self):
        self.__loadConfigUIFunc(None)
    
    def __loadUserConfigUIFunc(self):
        config_file_name = filedialog.askopenfilename()
        
        if config_file_name is None:
            messagebox.showinfo(title = "Load from User Config", message = "No file is selected.")
            return
        
        self.__loadConfigUIFunc(config_file_name)
        
    def __saveUserConfigUIFunc(self):
        (json_dict, error_message) = self.parent.config_form.getFullConfigJson()
        
        # Invalid input in the form
        if error_message:
            messagebox.showinfo(title = "Save user config", message = "Failed to save the user config. Input is invalid. Error message: " + error_message)
            return
        
        raw_json = json.dumps(json_dict)
        
        # Generate current time as the default text file name
        current_time = datetime.now().strftime("vcu_config_%Y-%d-%m-%H_%M_%S")
        print(current_time)
        
        # Open a file dialog to choose the save location
        file_path = filedialog.asksaveasfilename(initialfile=current_time, 
                defaultextension=".json", 
                filetypes=[("JSON file", "*.json"), ("All files", "*.*")])

        if file_path is None:
            return # No path is selected
            
        try:
            file = open(file_path, 'w')
            file.write(raw_json)
            file.close()
        except Exception as error:
            messagebox.showinfo(title = "Error", message = "Failed to save config to file. Error:" + str(error))
    
    def __loadConfigUIFunc(self, user_config_path):
        (result, errorMessage) = self.parent.configReader.readConfigFile(user_config_path)

        # If the config is already loaded, warn the user that this will overwrite the current form
        if self.parent.configFormLoaded:
            answer = messagebox.askquestion("Overwriting Current Config", "Are you sure you would like to load the config? \n Unsaved changes WILL be discarded.")
            if answer != "yes":
                return

        if result is None:
            messagebox.showinfo(title = "Load from Config", message = "Cannot load the config. Please make sure that a correct config is placed in the path: " + self.configReader.configPath + ". Error Info: " + errorMessage)
            return
        messagebox.showinfo(title = "Load from Config", message = "Load Config was successful!")
        self.parent.onConfigFormLoaded(result)
        
    def disableSaveConfigButton(self):
        self.save_user_config_button.configure(fg_color = "grey25", state = "disabled")
    
    def enableSaveConfigButton(self):
        self.save_user_config_button.configure(fg_color = ThemeManager.theme['CTkButton']['fg_color'], 
                                             state = "normal")