# Utility functions that are used by more than one module

# Check if a field is valid.
# returns (Result, Error Message)
def checkTypeValidity(type: str, value: any) -> tuple[bool, str]:
    match type:
        case "uint8_t":
            return checkNumber(0, 255, value)
        case "uint16_t":
            return checkNumber(0, 65535, value)
        case "uint32_t":
            return checkNumber(0, 4294967295, value)
        case "int8_t":
            return checkNumber(-128, 127, value)
        case "int16_t":
            return checkNumber(-32768, 32767, value)
        case "int32_t":
            return checkNumber(-2147483648, 2147483647, value)
        case "bool":
            if isinstance(value, bool):
                return (True, None)
            else:
                return (False, "value is not a bool")
        case "GPIOPort":
            return checkGPIOPort(value)
        case "GPIOPinNum":
            return checkNumber(1, 13, value)
        case _:
            return (False, "Type not found")

# Check if a number is valid.
# returns (Result, Error Message)
def checkNumber(min: int, max: int, value: any) -> tuple[bool, str]:
    if not isinstance(value, int):
        return (False, "value is not a number")
    if value >= min and value <= max:
        return (True, None)
    else:
        return (False, "value is out of range. Minimum: " + str(min) + ", Maximum: " + str(max))

# Check if a GPIO port is valid.
# returns (Result, Error Message)
def checkGPIOPort(value: any) -> tuple[bool, str]:
    if not isinstance(value, str):
        return (False, "value is not a string")
    if len(value) != 1:
        return (False, "value is not a character (i.e. string length is not one)")
    if value not in "ABCD":
        return (False, "Invalid GPIO Port")
    return (True, None)