from typing import Set, Dict, Any
import json

class ConfigReader:
    fieldTypes: Set[str] = {"uint8_t", 
            "uint8_t",
            "uint16_t", 
            "uint32_t", 
            "int8_t", 
            "int16_t", 
            "int32_t",
            "bool",
            "GPIOPort",
            "GPIOPinNum"}
    
    # Check if a number is valid.
    # returns (Result, Error Message)
    def __checkNumber(self, min: int, max: int, value: any) -> tuple[bool, str]:
        if not isinstance(value, int):
            return (False, "value is not a number")
        if value >= min and value <= max:
            return (True, None)
        else:
            return (False, "value is out of range")
    
    # Check if a GPIO port is valid.
    # returns (Result, Error Message)
    def __checkGPIOPort(self, value: any) -> tuple[bool, str]:
        if not isinstance(value, str):
            return (False, "value is not a string")
        if len(value) != 1:
            return (False, "value is not a character (i.e. string length is not one)")
        if value not in "ABCD":
            return (False, "Invalid GPIO Port")
        return (True, None)

    # Check if a field is valid.
    # returns (Result, Error Message)
    def __checkField(self, type: str, value: any) -> tuple[bool, str]:
        match type:
            case "uint8_t":
                return self.__checkNumber(0, 255, value)
            case "uint16_t":
                return self.__checkNumber(0, 65535, value)
            case "uint32_t":
                return self.__checkNumber(0, 4294967295, value)
            case "int8_t":
                return self.__checkNumber(-128, 127, value)
            case "int16_t":
                return self.__checkNumber(-32768, 32767, value)
            case "int32_t":
                return self.__checkNumber(-2147483648, 2147483647, value)
            case "bool":
                return isinstance(value, bool)
            case "GPIOPort":
                return self.__checkGPIOPort(value)
            case "GPIOPinNumber":
                return self.__checkNumber(1, 13, value)
    
    # Accepts a file path
    # Returns a dictionary of fieldName to (fieldType, fieldValue, description). Otherwise, return None and the error message
    def readConfigFile(self, configPath: str) -> tuple[Dict[str, tuple[str, Any, str]], str]:
        # Open the meta config file. If err, return err
        try:
            configFile = open(configPath, "r")
        except OSError as error:
            return (None, "Error opening the meta config file. Info: " + repr(error))
        try:
            configJson = json.load(configFile)
        except Exception as error:
            return (None, "Error when parsing the meta config file to a json object. Info: " + repr(error))
        
        return self.readConfigJson(configJson)

    # Accepts a json object
    # Returns a dictionary of fieldName to (fieldType, fieldValue, description). Otherwise, return None and the error message
    def readConfigJson(self, configJson) -> tuple[Dict[str, tuple[str, Any, str]], str]:
        config = dict()
        
        fields = configJson.get("fields")
        if not fields:
            return (None, "The item \"field\" is not found in the json file.")
        
        for field in fields:
            # Check if field type is valid
            fieldType = field.get("type")
            if not fieldType:
                return (None, "Field type of " + field + " in the config not found")
            
            if fieldType not in self.fieldTypes:
                return (None, "Field type of " + field + " is invalid")
            
            # Check if field value is vaild
            fieldValue = field.get("value")
            if not fieldValue:
                return (None, "Field value of " + field + " in the config not found")
            
            (result, errorMessage) = self.__checkField(fieldType, fieldValue)
            if not result:
                return (None, "Field value of " + field + " is out of range. Info: " + errorMessage)
            
            # Check if field description is valid
            fieldDescription = field.get("description")
            if not fieldDescription:
                return (None, "Field description of " + field + " in the config not found")

            # Add the pair to the config dictionary
            key = field
            value = (fieldType, fieldValue, fieldDescription)
            config[key] = value

        return (config, None)
    
    # Given a dictionary of fieldName to (fieldType, fieldValue, description), return a Json string of raw config (i.e. key-value pair of fieldName to fieldValue)
    def TurnConfigDictToRawConfigJson(self, configDict: Dict[str, tuple[str, Any, str]]) -> str:
        rawConfigDict = dict()
        for fieldName in configDict:
            (_, fieldValue, _) = configDict[fieldName]
            rawConfigDict[fieldName] = fieldValue

        return json.dumps(rawConfigDict)
    
    
