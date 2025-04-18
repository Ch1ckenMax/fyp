import customtkinter
from src.gui_src.gui_config_modifier_frame import ConfigModifierFrame
from src.gui_src.gui_calibrator_frame import CalibratorFrame
from src.gui_src.gui_log_viewer import LogViewerFrame

class GUI:
    def __init__(self,
                configReader,
                stlinkInterface,
                write_to_flash_memory_address):
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
        logViewerTab = tabview.add("Log Viewer")
        tabview._segmented_button.grid(sticky="W")

        # Add Frame to Tab
        configModFrame = ConfigModifierFrame(configModifierTab, configReader, stlinkInterface, write_to_flash_memory_address)
        configModFrame.pack(fill = "both", expand = True)

        logViewerFrame = LogViewerFrame(logViewerTab, stlinkInterface)
        logViewerFrame.pack(fill = "both", expand = True)
        
        calibratorFrame = CalibratorFrame(calibratorTab, configModFrame, logViewerFrame)
        calibratorFrame.pack(fill = "both", expand = True)
    
    def startGUILoop(self):
        self.root.mainloop()