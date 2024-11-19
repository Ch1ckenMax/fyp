import customtkinter

from src.utils import checkTypeValidity

class ConfigFormFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent, config_dict, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)

        self.config_dict = config_dict

        # Stores the widget of each field
        self.field_widget_list = []

        # Add the row for version first. Then remove the key for version for now.
        self.config_version = config_dict["version"]
        self.version_row = ConfigFormVersionRowFrame(self, self.config_version, fg_color = "grey10")
        self.version_row.grid(row = 0, column = 0, padx = 2, pady = 5, sticky = "W")

        config_dict.pop("version", None)

        # Generate for each field
        for (index, name) in enumerate(config_dict):
            # Special row for config version number

            new_row_frame = None
            (field_type, _, _) = config_dict[name]
            
            match field_type:
                case "uint8_t":
                    new_row_frame = ConfigFormNumberRowFrame(self, config_dict, name, height = 2)
                case "uint16_t":
                    new_row_frame = ConfigFormNumberRowFrame(self, config_dict, name, height = 2)
                case "uint32_t":
                    new_row_frame = ConfigFormNumberRowFrame(self, config_dict, name, height = 2)
                case "int8_t":
                    new_row_frame = ConfigFormNumberRowFrame(self, config_dict, name, height = 2)
                case "int16_t":
                    new_row_frame = ConfigFormNumberRowFrame(self, config_dict, name, height = 2)
                case "int32_t":
                    new_row_frame = ConfigFormNumberRowFrame(self, config_dict, name, height = 2)
                case "bool":
                    new_row_frame = ConfigFormBoolRowFrame(self, config_dict, name, height = 2)
                case "GPIOPort":
                    new_row_frame = ConfigFormGPIOPortRowFrame(self, config_dict, name, height = 2)
                case "GPIOPinNum":
                    new_row_frame = ConfigFormGPIOPinNumRowFrame(self, config_dict, name, height = 2)
                case _:
                    raise Exception("Encountered unknown type when creating a row in config form. Please raise to developers. type: " + field_type)
            
            self.field_widget_list.append(new_row_frame)
            self.field_widget_list[index].grid(row = index + 1, column = 0, padx = 2, pady = 2, sticky = "W")
        
        # Add the version back to the dict
        config_dict["version"] = self.config_version

    # Return (Value only config json from the form, Error Message)
    def getValueOnlyConfigJson(self) -> tuple[dict[str, any], str]:
        new_config_dict = dict()
        new_config_dict["version"] = self.config_version
        failed = False
        fail_message = ""

        for field_widget in self.field_widget_list:
            (success, dict_or_error_message) = field_widget.getValidInputFieldValue()

            if success and not failed:
                new_config_dict[field_widget.name] = dict_or_error_message
            elif success and failed:
                pass # noop. Do nothing.
            elif not success:
                failed = True
                fail_message = fail_message + dict_or_error_message + '\n'
        
        if not failed:
            return (new_config_dict, None)
        else:
            return (None, fail_message)
                
# Abstract class. Do NOT make an instance with this class.
class AbstractConfigFormRowFrame(customtkinter.CTkFrame):
    def __init__(self, parent, config_dict, name, **kwargs):
        super().__init__(parent, **kwargs)
        self.name = name
        self.config_dict = config_dict
        (self.type, self.value, self.description) = config_dict[name]

        self.grid_columnconfigure(0, weight=160)
        self.grid_columnconfigure(1, weight=20)
        self.grid_columnconfigure(2, weight=160)
        self.grid_columnconfigure(3, weight=600)

        # Field name
        self.field_name_widget = customtkinter.CTkLabel(self, text = name, wraplength = 140, width = 160, padx = 2)
        self.field_name_widget.grid(row = 0, column = 0)

        # Input field
        self.input_field_widget = self.getInputFieldWidget()
        self.input_field_widget.grid(row = 0, column = 1, sticky = "e")

        # Field type
        self.field_type_widget = customtkinter.CTkLabel(self, text = self.type, wraplength = 150, width = 160)
        self.field_type_widget.grid(row = 0, column = 2)

        # Description
        self.description_widget = customtkinter.CTkLabel(self, text = self.description, wraplength = 550, width = 600, anchor = "w", padx = 5, justify = "left")
        self.description_widget.grid(row = 0, column = 3)

    # Abstract member functions

    # Get the input field widget
    def getInputFieldWidget(self) -> customtkinter.CTkBaseClass:
        raise Exception("Please implement getInputFieldWidget")

    # Get the value from the input field
    def getRawInputFieldValue(self) -> any:
        raise Exception("Please implement getRawInputFieldValue")
    
    def getValidInputFieldValue(self) -> tuple[bool, any]:
        raise Exception("Please implement getValidInputFieldValue")
    
class ConfigFormNumberRowFrame(AbstractConfigFormRowFrame):
    def __init__(self, parent, config_dict, name, **kwargs):
        super().__init__(parent, config_dict, name, **kwargs)
        self.parent = parent

    def getInputFieldWidget(self) -> customtkinter.CTkBaseClass:
        input_field = customtkinter.CTkEntry(self, corner_radius = 1, height = 1, width = 60)
        input_field.insert(0, str(self.value))
        return input_field
    
        # Get the value from the input field
    def getRawInputFieldValue(self) -> any:
        return self.input_field_widget.get()
    
    # Get the valid input field value
    # Returns (Success, Value | Error Message)
    def getValidInputFieldValue(self) -> tuple[bool, any]:
        input_field_value = None
        try:
            input_field_value = int(self.getRawInputFieldValue())
        except:
            return (False, self.name + ": the given value is not a number")
        
        (success, error_message) = checkTypeValidity(self.type, input_field_value)
        
        if success:
            return (True, input_field_value)
        else:
            return (False, self.name + ": " + error_message)

class ConfigFormBoolRowFrame(AbstractConfigFormRowFrame):
    def __init__(self, parent, config_dict, name, **kwargs):
        super().__init__(parent, config_dict, name, **kwargs)
        self.parent = parent

    def getInputFieldWidget(self) -> customtkinter.CTkBaseClass:
        input_field = customtkinter.CTkCheckBox(self, height = 1, width = 60, text = "")
        if self.value is True:
            input_field.select()

        return input_field
    
        # Get the value from the input field
    def getRawInputFieldValue(self) -> any:
        return self.input_field_widget.get()
    
    def getValidInputFieldValue(self) -> tuple[bool, any]:
        return (True, self.getRawInputFieldValue())

class ConfigFormGPIOPortRowFrame(AbstractConfigFormRowFrame):
    def __init__(self, parent, config_dict, name, **kwargs):
        super().__init__(parent, config_dict, name, **kwargs)
        self.parent = parent

    def getInputFieldWidget(self) -> customtkinter.CTkBaseClass:
        input_field = customtkinter.CTkOptionMenu(self, values=["A", "B", "C", "D"], corner_radius = 1, height = 1, width = 60)
        input_field.set(self.value)

        return input_field
    
        # Get the value from the input field
    def getRawInputFieldValue(self) -> any:
        return self.input_field_widget.get()
    
    def getValidInputFieldValue(self) -> tuple[bool, any]:
        return (True, self.getRawInputFieldValue())

class ConfigFormGPIOPinNumRowFrame(AbstractConfigFormRowFrame):
    def __init__(self, parent, config_dict, name, **kwargs):
        super().__init__(parent, config_dict, name, **kwargs)
        self.parent = parent

    def getInputFieldWidget(self) -> customtkinter.CTkBaseClass:
        input_field = customtkinter.CTkOptionMenu(self, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"], corner_radius = 1, height = 1, width = 60)
        input_field.set(str(self.value))

        return input_field
    
        # Get the value from the input field
    def getRawInputFieldValue(self) -> any:
        return int(self.input_field_widget.get())
    
    def getValidInputFieldValue(self) -> tuple[bool, any]:
        return (True, self.getRawInputFieldValue())
    
class ConfigFormVersionRowFrame(customtkinter.CTkFrame):
    def __init__(self, parent, version, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_columnconfigure(0, weight=180)
        self.grid_columnconfigure(1, weight=160)
        self.grid_columnconfigure(2, weight=760)

        self.field_name_widget = customtkinter.CTkLabel(self, text = "Config Version", wraplength = 140, width = 220, padx = 2, font = customtkinter.CTkFont(weight = "bold"))
        self.field_name_widget.grid(row = 0, column = 0)

        self.field_name_widget = customtkinter.CTkLabel(self, text = version, wraplength = 140, width = 160, padx = 2, font = customtkinter.CTkFont(weight = "bold"))
        self.field_name_widget.grid(row = 0, column = 1)

        self.field_name_widget = customtkinter.CTkLabel(self, text = "The version number of the default config must match the VCU's version. The VCU will check whether the version number matches before loading the config.", 
                                                        wraplength = 525, 
                                                        width = 600, 
                                                        anchor = "w", 
                                                        padx = 5, 
                                                        pady = 10,
                                                        justify = "left",
                                                        font = customtkinter.CTkFont(weight = "bold"))
        self.field_name_widget.grid(row = 0, column = 2)
    
# TODO: create some functions for the calibrator to change the fields.
# The rows should be tracked in a dict instead of a list.
# Each row should have a function to change its own value.