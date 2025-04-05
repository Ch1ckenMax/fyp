import customtkinter
import tkinter

BUTTON_WIDTH = 200
APPS_THEORTICAL_MAX = 4095

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
        
        # Instructions
        instruction_text = """
                Instructions\n 
                1. Enable Calibrator Logs in Config by selecting the CalibratorLogEnabled option\n
                2. Connect the VCU to the computer\n
                3. Start the Log Viewer\n
                4. The current status of the VCU will be shown above.\n\n
                
                To calibrate:\n
                1. Make sure a config is loaded in the Config Modifier tab\n
                2. Start the Log Viewer
                3. Release the throttle pedal and click Record Minimum\n
                4. Fully press the throttle pedal and click Record Maximum\n
                5. Stop the Log Viewer\n
                6. Upload the config to the VCU\n
                7. Start the log viewer again, and verify the changes in this tab"""
        self.instruction_text = customtkinter.CTkLabel(self, text = instruction_text, fg_color = "dimgray", corner_radius = 5, pady = 10)
        self.instruction_text.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "new")
        
        # Info
        self.apps1_frame = ItemListFrame(self, "Throttle Pin 0")
        self.apps1_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.apps2_frame = ItemListFrame(self, "Throttle Pin 1")
        self.apps2_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "new")
        
    def __updateAppsMin(self):
        print("updateAppsMin TODO")
        self.config_mod_frame.config_form.updateAPPSMinValueInForm(200,700)
        
    def __updateAppsMax(self):
        print("updateAppsMax TODO")
        
class ItemListFrame(customtkinter.CTkFrame):
    def __init__(self, parent, name):
        super().__init__(parent)
        
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        
        # Title
        self.title = customtkinter.CTkLabel(self, text = name, font = customtkinter.CTkFont(weight = "bold"), fg_color = "dimgray", corner_radius = 5)
        self.title.grid(row = 0, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = "news")
        
        # Bar
        self.apps_bar = ItemProgressBar(self)
        self.apps_bar.grid(row = 1, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = "new")
        
        # Data
        self.min_value = ItemFieldFrame(self, "Min Value", "To be updated")
        self.min_value.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.max_value = ItemFieldFrame(self, "Max Value", "To be updated")
        self.max_value.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.raw_value = ItemFieldFrame(self, "Raw Value", "To be updated")
        self.raw_value.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "new")
        
        self.torque = ItemFieldFrame(self, "Torque", "To be updated")
        self.torque.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "new")
        
    def updateValues(self, minimum, maximum, raw, torque, max_torque):
        self.apps_bar.update(minimum, maximum, raw)
        self.min_value.updateValue(minimum)
        self.max_value.updateValue(maximum)
        self.raw_value.updateValue(raw)
        
        torque_value = f"{torque / 10} / {max_torque / 10} Nm"
        self.torque.updateValue(torque_value)
        
class ItemFieldFrame(customtkinter.CTkFrame):
    def __init__(self, parent, name, default_value):
        super().__init__(parent)
        self.name = name

        self.grid_columnconfigure(0, weight=160)
        self.grid_columnconfigure(1, weight=20)

        # item name
        self.name_widget = customtkinter.CTkLabel(self, text = name, wraplength = 140, width = 160, padx = 2, font = customtkinter.CTkFont(weight = "bold"))
        self.name_widget.grid(row = 0, column = 0)

        # Input field
        self.value_widget = customtkinter.CTkLabel(self, text = str(default_value), wraplength = 140, width = 160, padx = 2)
        self.value_widget.grid(row = 0, column = 1, sticky = "e")
        
    def updateValue(self, value):
        self.value_widget.configure(text = str(value))
        
class ItemProgressBar(customtkinter.CTkProgressBar):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(fg_color="black")
        self.configure(border_color="blue")
        
    def update(self, minimum, maximum, raw_value):
        if raw_value < minimum or raw_value > maximum:
            self.configure(progress_color="red")
        else:
            self.configure(progress_color="blue")
            
        self.set(raw_value / APPS_THEORTICAL_MAX)
    