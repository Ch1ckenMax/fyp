import subprocess

# Constants
ST_LINK_EXE_PATH = ".\\externlib\\stlink-1.7.0-x86_64-w64-mingw32\\bin\\"
MEMORY_SIZE = 0x20000

class VCUInterface:
    # def __init__(self, STLinkExecutablePath =  ".\\externlib\\stlink-1.7.0-x86_64-w64-mingw32\\bin\\": str, memorySize = 0):
    #     self.STLinkExecutablePath = STLinkExecutablePath
    #     self.memorySize = memorySize
    
    def HasConnection(self) -> tuple[bool, str]:
        result = subprocess.run([ST_LINK_EXE_PATH + "st-info.exe", "--probe"], capture_output = True)
        
        hasConnection = result.returncode == 0 and result.stdout[:7] == b"Found 1" and result.stderr == b""
        error = None if hasConnection else (result.stdout + result.stderr)

        return (hasConnection, error)
    
    def WriteToFlash(self, content: str, memoryAddress: int) -> tuple[bool, str]:
        # Bound checks
        if memoryAddress < self.flashMinAddress or memoryAddress >= self.flashMaxAddress:
            return (False, "Memory address is out of bound. Please raise to developers.")
        
        try:
            binary = content.encode("ascii")
        except UnicodeEncodeError as error:
            return (False, "Error encoding the content to ascii. Info: " + error)
        
        
        
        # Open file
        try:
            binaryTempFile = open("tempconfig.bin", "wxb")
        except IOError as error:
            return (False, "Failed to create a temporary file. Please run the program as an adminstrator. Info: " + error.strerror)
        except:
            return (False, "Failed to create a temporary file. Please run the program as an adminstrator.")

        # Check if you can read the file

        # If the file can be read, check if the file is larger than the max flash
        
        # If write success, 0 is returned. Else, 1 is returned.

        return (True, "")
        
