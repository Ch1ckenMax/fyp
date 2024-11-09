from tkinter import messagebox
import customtkinter
from customtkinter import ThemeManager

BUTTON_WIDTH = 200

class ConfigVCUButtonFrame(customtkinter.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 20)
        self.grid_rowconfigure(2, weight = 20)
        self.grid_columnconfigure(0, weight = 1)

        # Title
        self.title = customtkinter.CTkLabel(self, text = "VCU Control Pane", bg_color = "grey25", padx = 5, pady = 5)
        self.title.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "new")

        # Button for checking connection
        self.has_connection_button = customtkinter.CTkButton(self, text="Check STM32 Board Connection", command=self.__hasConnectionUIFunc, width = BUTTON_WIDTH)
        self.has_connection_button.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "new")

        # Button for writing to flash of STM32
        self.write_to_flash_button = customtkinter.CTkButton(self, text="Write Config to STM32", command=self.__writeToFlashUIFunc, width = BUTTON_WIDTH)
        self.write_to_flash_button.grid(row = 2, column = 0,  padx = 5, pady = 5, sticky = "new")

    def __hasConnectionUIFunc(self):
        (result, errorMessage) = self.parent.stlinkInterface.HasConnection()

        if result:
            messagebox.showinfo(title = "Connection", message = "There is connection with exactly one STM32 board.")
        else:
            messagebox.showinfo(title = "Connection", message = "STM32 board not found. Error Info: " + errorMessage)

    def __writeToFlashUIFunc(self):
        (value_only_dict, error_message) = self.parent.config_form.getValueOnlyConfigJson()

        print(value_only_dict)
        if value_only_dict is None:
            messagebox.showinfo(title = "Write to Flash", message = "The config in the config form is invalid. Please check the values: \n " + error_message)
            return

        (result, error_message) = self.parent.stlinkInterface.WriteToFlash(str(value_only_dict), self.parent.write_flash_memory_address, ".\\tempbuf.bin")

        if result:
            messagebox.showinfo(title = "Write to Flash", message = "Write Success!")
        else:
            messagebox.showinfo(title = "Write to Flash", message = "Write Failed. Error Info: " + error_message)

    def disableWriteToFlashButton(self):
        self.write_to_flash_button.configure(fg_color = "grey25", state = "disabled")
    
    def enableWriteToFlashButton(self):
        self.write_to_flash_button.configure(fg_color = ThemeManager.theme['CTkButton']['fg_color'], 
                                             state = "normal")