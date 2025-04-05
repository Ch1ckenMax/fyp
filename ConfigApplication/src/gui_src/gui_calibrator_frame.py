import customtkinter

BUTTON_WIDTH = 200

class CalibratorFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, config_mod_frame, log_viewer_frame):
        super().__init__(parent)
        
        self.config_mod_frame = config_mod_frame
        self.log_viewer_frame = log_viewer_frame
        
        self.grid_columnconfigure(0, weight = 9)
        self.grid_columnconfigure(1, weight = 1)
        
        # Buttons
        self.start_log_button = customtkinter.CTkButton(self, text="Record Minimum", command=self.__updateAppsMin, width = BUTTON_WIDTH)
        self.start_log_button.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "new")

        self.stop_log_button = customtkinter.CTkButton(self, text="Record Maximum", command=self.__updateAppsMax, width = BUTTON_WIDTH)
        self.stop_log_button.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "new")
        
    def __updateAppsMin(self):
        print("updateAppsMin TODO")
        self.config_mod_frame.config_form.updateAPPSMinValueInForm(200,700)
        
    def __updateAppsMax(self):
        print("updateAppsMax TODO")