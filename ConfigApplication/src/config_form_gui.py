from tkinter import messagebox
import customtkinter

class ConfigFormFrame(customtkinter.CTkFrame):
     def __init__(self, parent, configDict, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Stores the widget of each field
        self.fieldWidget = []

        # Generate for each field
        for (index, name) in enumerate(configDict):
            (type, value, description) = configDict[name]
            print(type, value, description)

            self.fieldWidget.append(customtkinter.CTkLabel(self, text=str(type) + str(value) + str(description)))
            self.fieldWidget[index].grid(row = index, column = 0)

        