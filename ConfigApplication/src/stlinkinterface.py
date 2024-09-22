import subprocess

# Constants
ST_LINK_EXE_PATH = ".\\externlib\\stlink-1.7.0-x86_64-w64-mingw32\\bin\\"

class VCUInterface:
    def __init__(self, flashMinAddress: int, flashMaxAddress: int):
        self.flashMinAddress = flashMinAddress
        self.flashMaxAddress = flashMaxAddress
    
    def HasConnection(self) -> tuple[bool, str]:
        result = subprocess.run([ST_LINK_EXE_PATH + "st-info.exe", "--probe"], capture_output = True)
        
        hasConnection = result.returncode == 0 and result.stdout[:7] == b"Found 1" and result.stderr == b""
        error = None if hasConnection else (result.stdout + result.stderr)

        return (hasConnection, error)
    
    def WriteHexFileToFlash(self, filePath: str, memoryAddress: int) -> tuple[bool, str]:
        # Bound checks
        if memoryAddress < self.flashMinAddress or memoryAddress >= self.flashMaxAddress:
            return (False, "Memory address is out of bound. Please raise to developers.")
        
        # Check if you can read the file

        # If the file can be read, check if the file is larger than the max flash
        
        return (True, "")
        
