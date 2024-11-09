from typing import Set, Dict, Any
import json

from src.utils import checkTypeValidity

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
    
    def __init__(self, configPath: str):
        self.configPath = configPath
    
    # Accepts a file path
    # Returns a dictionary of fieldName to (fieldType, fieldValue, description). Otherwise, return None and the error message
    def readConfigFile(self) -> tuple[Dict[str, tuple[str, Any, str]], str]:
        # Open the meta config file. If err, return err
        try:
            configFile = open(self.configPath, "r")
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
        
        version = configJson.get("version")
        if not version:
            return (None, "Config version is not found in the json file.")
        
        config["version"] = str(version)
        
        fields = configJson.get("fields")
        if not fields:
            return (None, "The item \"field\" is not found in the json file.")
        
        for fieldName in fields:
            field = fields[fieldName]

            # Check if field type is valid
            fieldType = field.get("type")
            if fieldType is None:
                return (None, "Field type of " + fieldName + " in the config not found")
            
            if fieldType not in self.fieldTypes:
                return (None, "Field type of " + fieldName + " is invalid")
            
            # Check if field value is vaild
            fieldValue = field.get("value")
            if fieldValue is None:
                return (None, "Field value of " + fieldName + " in the config not found")

            (result, errorMessage) = checkTypeValidity(fieldType, fieldValue)

            if result is None:
                return (None, "Field value of " + fieldName + " is out of range. Info: " + errorMessage)
            
            # Check if field description is valid
            fieldDescription = field.get("description")
            if fieldDescription is None:
                return (None, "Field description of " + field + " in the config not found")

            # Add the pair to the config dictionary
            key = fieldName
            value = (fieldType, fieldValue, fieldDescription)
            config[key] = value

        return (config, None)
    
    # Given a dictionary of fieldName to (fieldType, fieldValue, description), return a Json string of raw config (i.e. key-value pair of fieldName to fieldValue)
    def TurnConfigDictToRawConfigJson(self, configDict: Dict[str, tuple[str, Any, str]]) -> str:
        rawConfigDict = dict()
        for fieldName in configDict:
            if fieldName == "version":
                rawConfigDict[fieldName] = configDict["version"]
            else:
                (_, fieldValue, _) = configDict[fieldName]
                rawConfigDict[fieldName] = fieldValue

        return json.dumps(rawConfigDict)
    

