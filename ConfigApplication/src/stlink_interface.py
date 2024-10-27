import subprocess

class VCUInterface:
    def __init__(self, STLinkExecutablePath: str, memorySize: int, memoryStartAddress: int):
        self.STLinkExecutablePath = STLinkExecutablePath
        self.memorySize = memorySize
        self.memoryStartAddress = memoryStartAddress
    
    def HasConnection(self) -> tuple[bool, str]:
        result = subprocess.run([self.STLinkExecutablePath + "st-info.exe", "--probe"], capture_output = True)
        
        hasConnection = result.returncode == 0 and result.stdout[:7] == b"Found 1" and result.stderr == b""
        error = None if hasConnection else (result.stdout + result.stderr)

        return (hasConnection, str(error))
    
    # Return (True, None) if success
    # Return (False, errorMessageString) if fail
    def WriteToFlash(self, content: str, memoryAddress: int, binaryTempFilePath: str) -> tuple[bool, str]:
        # Bound checks
        if memoryAddress < self.memoryStartAddress or memoryAddress >= self.memoryStartAddress + self.memorySize:
            return (False, "Memory address is out of bound. Please raise to developers.")
        
        try:
            binary = (content + '\0').encode("ascii") # Add a null character at the end to indicate end of string
        except UnicodeEncodeError as error:
            return (False, "Error encoding the content to ascii. Info: " + repr(error))
        
        # Size check
        if len(binary) > self.memorySize:
            return (False, "Config size is more than allowed. Allowed size: ", self.memorySize, ", Config size: ", len(binary))
        
        # Open a file
        try:
            binaryTempFile = open(binaryTempFilePath, "wb")
        except Exception as error:
            return (False, "Failed to create a temporary file. Please run the program as an adminstrator. Info: ", error)
        
        binaryTempFile.write(binary)
        binaryTempFile.close()

        result = subprocess.run([self.STLinkExecutablePath + "st-flash.exe", "write", binaryTempFilePath, hex(memoryAddress)], capture_output = True)

        if result.returncode == 0: # Success
            return (True, None)
        else:
            return (False, "Failed to flash the config to memory. Info: " + str(result.stdout + result.stderr))
        
