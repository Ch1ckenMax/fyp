import customtkinter
from src.config_modifier_frame_gui import ConfigModifierFrame

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

        configModifierTab = tabview.add("Config Modifier")
        calibratorTab = tabview.add("Calibrator")
        tabview._segmented_button.grid(sticky="W")

        # Add Frame to Tab
        configModFrame = ConfigModifierFrame(configModifierTab, configReader, stlinkInterface)
        configModFrame.pack(fill = "both", expand = True)
    
    def startGUILoop(self):
        self.root.mainloop()