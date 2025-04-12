import customtkinter
import tkinter
from tkinter import messagebox

BUTTON_WIDTH = 200
APPS_THEORTICAL_MAX = 4095

class CalibratorFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, config_mod_frame, log_viewer_frame):
        super().__init__(parent)
        
        self.config_mod_frame = config_mod_frame
        self.log_viewer_frame = log_viewer_frame
        
        # Send the self reference to the log viewer frame
        self.log_viewer_frame.saveRefToCalibratorFrame(self)
        
        self.grid_columnconfigure(0, weight = 9)
        self.grid_columnconfigure(1, weight = 1)
        
        self.calibrator_buttons = customtkinter.CTkFrame(self)
        self.calibrator_buttons.grid(row = 0, column = 1, sticky = "new", rowspan = 5)
        
        # Title
        self.title = customtkinter.CTkLabel(self.calibrator_buttons, text = "Record in Config Form", bg_color = "grey25", padx = 5, pady = 5)
        self.title.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "new")
        
        # Buttons
        self.start_log_button = customtkinter.CTkButton(self.calibrator_buttons, text="Record Throttle Minimum", command=self.__updateAppsMin, width = BUTTON_WIDTH)
        self.start_log_button.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "new")

        self.stop_log_button = customtkinter.CTkButton(self.calibrator_buttons, text="Record Throttle Maximum", command=self.__updateAppsMax, width = BUTTON_WIDTH)
        self.stop_log_button.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.stop_log_button = customtkinter.CTkButton(self.calibrator_buttons, text="Record Brake Minimum", command=self.__updateBrakeMin, width = BUTTON_WIDTH)
        self.stop_log_button.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.stop_log_button = customtkinter.CTkButton(self.calibrator_buttons, text="Record Brake Maximum", command=self.__updateBrakeMax, width = BUTTON_WIDTH)
        self.stop_log_button.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "new")

        self.stop_log_button = customtkinter.CTkButton(self.calibrator_buttons, text="Record Regen Minimum", command=self.__updateRegenMin, width = BUTTON_WIDTH)
        self.stop_log_button.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.stop_log_button = customtkinter.CTkButton(self.calibrator_buttons, text="Record Regen Maximum", command=self.__updateRegenMax, width = BUTTON_WIDTH)
        self.stop_log_button.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "new")
        
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
        self.instruction_text.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "new")
        
        # Info
        self.apps1_frame = TorqueItemListFrame(self, "Throttle Pin 0")
        self.apps1_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.apps2_frame = TorqueItemListFrame(self, "Throttle Pin 1")
        self.apps2_frame.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.brake_frame = ItemListFrame(self, "Brake")
        self.brake_frame.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "new")
        
        self.regen_frame = TorqueItemListFrame(self, "Regen Knob")
        self.regen_frame.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "new")
        
        # Raw values received
        self.apps1_val = None
        self.apps2_val = None
        self.brake_val = None
        self.regen_val = None
        
    def updateBySensorLogLine(self, log_line: str):
        # Separate the log line by space
        log_line_splitted_list = log_line.split(' ')
        
        # Return if the size does not match.
        # The logs are formatted as the following:
        # timestamp [SENSOR] max min val theortical_max ...
        # Hence, the valid number of elements in the list is given by:
        # 2 + 4 * number_of_analog_sensors
        valid_number_of_elements = 2 + 4 * 4
        
        if len(log_line_splitted_list) != valid_number_of_elements:
            return
        
        # Remove logs that are not in the SENSOR level
        if log_line_splitted_list[1] != "[SENSOR]":
            return
        
        # Try casting to interger
        data = []
        try:
            for element in log_line_splitted_list[2:]:
                data.append(int(element))
        except ValueError:
            return
        
        self.apps1_frame.updateValues(data[0], data[1], data[2], data[3])
        self.apps2_frame.updateValues(data[4], data[5], data[6], data[7])
        self.brake_frame.updateValues(data[8], data[9], data[10], data[11])
        self.regen_frame.updateValues(data[12], data[13], data[14], data[15])
        
        self.apps1_val = data[2]
        self.apps2_val = data[6]
        self.brake_val = data[10]
        self.regen_val = data[14]
        
    def __updateAppsMin(self):
        if self.apps1_val is None or self.apps2_val is None:
                messagebox.showinfo(title = "Update Throttle Min", 
                    message = "No analog data is received from the VCU. Make sure that:\n1. SENSOR logs is enabled\n2. Log Viewer is turned on")
                
        self.config_mod_frame.config_form.updateAPPSMinValueInForm(self.apps1_val, self.apps2_val)
        
    def __updateAppsMax(self):
        if self.apps1_val is None or self.apps2_val is None:
                messagebox.showinfo(title = "Update Throttle Max", 
                    message = "No analog data is received from the VCU. Make sure that:\n1. SENSOR logs is enabled\n2. Log Viewer is turned on")
                
        self.config_mod_frame.config_form.updateAPPSMaxValueInForm(self.apps1_val, self.apps2_val)
        
    def __updateBrakeMin(self):
        if self.brake_val is None:
                messagebox.showinfo(title = "Update Brake Min", 
                    message = "No analog data is received from the VCU. Make sure that:\n1. SENSOR logs is enabled\n2. Log Viewer is turned on")
                
        self.config_mod_frame.config_form.updateBrakeMinValueInForm(self.brake_val)
        
    def __updateBrakeMax(self):
        if self.brake_val is None:
                messagebox.showinfo(title = "Update Brake Max", 
                    message = "No analog data is received from the VCU. Make sure that:\n1. SENSOR logs is enabled\n2. Log Viewer is turned on")
                
        self.config_mod_frame.config_form.updateBrakeMaxValueInForm(self.brake_val)
    
    def __updateRegenMin(self):
        if self.regen_val is None:
                messagebox.showinfo(title = "Update Regen Min", 
                    message = "No analog data is received from the VCU. Make sure that:\n1. SENSOR logs is enabled\n2. Log Viewer is turned on")
                
        self.config_mod_frame.config_form.updateRegenMinValueInForm(self.regen_val)
        
    def __updateRegenMax(self):
        if self.regen_val is None:
                messagebox.showinfo(title = "Update Regen Max", 
                    message = "No analog data is received from the VCU. Make sure that:\n1. SENSOR logs is enabled\n2. Log Viewer is turned on")
                
        self.config_mod_frame.config_form.updateRegenMaxValueInForm(self.regen_val)
        
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
        
        self.translated_value = ItemFieldFrame(self, "Torque", "To be updated")
        self.translated_value.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = "new")
        
    def updateValues(self, minimum, maximum, raw, translated_max):
        self.apps_bar.update(minimum, maximum, raw)
        self.min_value.updateValue(minimum)
        self.max_value.updateValue(maximum)
        self.raw_value.updateValue(raw)
        
        translated_value = translated_max * (raw - minimum) / (maximum - minimum)
        display_value = f"{translated_value:.1f} / {translated_max}"
        self.translated_value.updateValue(display_value)

# Sub-class of ItemListFrame for representing analog sensor that 
# has torque as the translated value.
class TorqueItemListFrame(ItemListFrame):
    def __init__(self, parent, *kwargs):
        super().__init__(parent, *kwargs)
        self.parent = parent
        
    def updateValues(self, minimum, maximum, raw, translated_max):
        self.apps_bar.update(minimum, maximum, raw)
        self.min_value.updateValue(minimum)
        self.max_value.updateValue(maximum)
        self.raw_value.updateValue(raw)
        
        translated_value = translated_max * (raw - minimum) / (maximum - minimum)
        display_value = f"{translated_value / 10:.1f} / {translated_max / 10} Nm"
        self.translated_value.updateValue(display_value)
        
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
        if raw_value < minimum:
            self.configure(progress_color="purple")
        elif raw_value > maximum:
            self.configure(progress_color="red")
        else:
            self.configure(progress_color="blue")
            
        self.set(raw_value / APPS_THEORTICAL_MAX)
    