import subprocess
import signal
import os

class VCUInterface:
    def __init__(self, st_link_executable_path: str, 
                st_programmer_executable: str, 
                rt_console: str,
                memory_size: int, 
                memory_start_address: int,
                st_system_clock_mhz: int):
        
        self.st_link_executable_path = st_link_executable_path
        self.st_programmer_executable = st_programmer_executable
        self.rt_console = rt_console
        self.memory_size = memory_size
        self.memory_start_address = memory_start_address
        self.st_system_clock_mhz = st_system_clock_mhz

        self.swv_log_reader_process_pid = None
    
    def HasConnection(self) -> tuple[bool, str]:
        try:
            result = subprocess.run([self.st_link_executable_path + "st-info.exe", "--probe"], capture_output = True, timeout = 1)
        except subprocess.TimeoutExpired as error:
            return (False, "Timed out.")
        
        has_connection = result.returncode == 0 and result.stdout[:7] == b"Found 1" and result.stderr == b""
        error = None if has_connection else (result.stdout + result.stderr)

        return (has_connection, str(error))
    
    # Return (True, None) if success
    # Return (False, errorMessageString) if fail
    def WriteToFlash(self, content: str, memoryAddress: int, binaryTempFilePath: str) -> tuple[bool, str]:
        # Bound checks
        if memoryAddress < self.memory_start_address or memoryAddress >= self.memory_start_address + self.memory_size:
            return (False, "Memory address is out of bound. Please raise to developers.")
        
        try:
            binary = (content + '\0').encode("ascii") # Add a null character at the end to indicate end of string
        except UnicodeEncodeError as error:
            return (False, "Error encoding the content to ascii. Info: " + repr(error))
        
        # Size check
        if len(binary) > self.memory_size:
            return (False, "Config size is more than allowed. Allowed size: ", self.memory_size, ", Config size: ", len(binary))
        
        # Open a file
        try:
            binaryTempFile = open(binaryTempFilePath, "wb")
        except Exception as error:
            return (False, "Failed to create a temporary file. Please run the program as an adminstrator. Info: ", repr(error).encode("utf-8"))
        
        binaryTempFile.write(binary)
        binaryTempFile.close()

        result = subprocess.run([self.st_link_executable_path + "st-flash.exe", "write", binaryTempFilePath, hex(memoryAddress)], capture_output = True)

        if result.returncode == 0: # Success
            return (True, None)
        else:
            return (False, str("Failed to flash the config to memory. Info: ") + str(result.stdout) + str(result.stderr))
    
    # Start a SWV Log Reader process and return its stdout and stderr
    def StartSWVLogReaderProcess(self) -> any:
        try:
            swv_log_reader_process = subprocess.Popen([
                            self.st_programmer_executable,
                            "-c", 
                            "port=swd", 
                            "-swv", 
                            "freq=" + str(self.st_system_clock_mhz), 
                            "portnumber=0", "-RA"],
                            text = True,
                            bufsize = 1,
                            stdin = subprocess.DEVNULL,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.STDOUT)
        except Exception as error:
            print(repr(error))
            return None
        
        self.swv_log_reader_process_pid = swv_log_reader_process.pid
        print("Process pid: ", self.swv_log_reader_process_pid)
        return swv_log_reader_process.stdout
    
    def StopSWVLogReaderProcess(self):
        if self.swv_log_reader_process_pid is None:
            return
        
        # subprocess's kill() or terminate() won't work because windows does not have SIGKILL or SIGTERM.
        # The subprocess module is too stupid to separate code for windows machine.
        # CTRL C event also does not work as it will propagate from the child process to the parent process
        # and kill the GUI altogether.
        # The only viable approaches are to:
        # 1. Use taskkill. However this method is flaky (does not work 100% time). Advantage is that if it works, it is killed instantly.
        # 2. Use wmic process where. It kills process by name, always works. Disadvantage is that it takes some time.
        # Hence, we adopt both approaches.
        try:
            subprocess.call(['taskkill', '/F', '/T', '/PID',  str(self.swv_log_reader_process_pid)])
        except Exception as error:
            print("DEBUG: task kill error")
            print(repr(error))

        try:
            # The nuclear option. In case it doesn't go down after taskkill:
            subprocess.run(['wmic', 'process', 'where', 'name = \"STM32_Programmer_CLI.exe\"', 'delete']) 
        except Exception as error: # If the above taskkill was sucessful, the exception will happen (FileNotFoundError)
            print("wmic nuke was no-op: ", error)
        
        self.swv_log_reader_process_pid = None


