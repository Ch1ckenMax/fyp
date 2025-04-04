import customtkinter
from threading import Thread
from tkinter import messagebox, filedialog
from datetime import datetime

LOG_TEXT_BOX_HEIGHT = 700
BUTTON_WIDTH = 100

class LogViewerFrame(customtkinter.CTkFrame):
    def __init__(self, parent,
                stlinkInterface):
        super().__init__(parent)

        self.stlink_interface = stlinkInterface

        # Thread for reading log
        self.log_reader_thread = None

        self.grid_columnconfigure(0, weight = 9)
        self.grid_columnconfigure(1, weight = 1)

        # Text box for showing the logs. Disabled by default. Will be enabled when the program connects with the STM32 board via STM32CubeProgrammer CLI
        self.log_text_box = customtkinter.CTkTextbox(self, height = LOG_TEXT_BOX_HEIGHT)
        self.log_text_box.insert("0.0", "Please click the connect button to start the program and read from the logs.\n")
        self.log_text_box.configure(state = "disabled")
        self.log_text_box.grid(row = 0, column = 0, rowspan = 3, padx = 5, pady = 5, sticky = "news")

        # Buttons
        self.start_log_button = customtkinter.CTkButton(self, text="Start/Restart Program", command=self.__readLogs, width = BUTTON_WIDTH)
        self.start_log_button.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "new")

        self.stop_log_button = customtkinter.CTkButton(self, text="Stop Logging", command=self.__stopLogs, width = BUTTON_WIDTH)
        self.stop_log_button.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "new")
        
        self.stop_log_button = customtkinter.CTkButton(self, text="Save Log to Text File", command=self.__saveLogToFile, width = BUTTON_WIDTH)
        self.stop_log_button.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "new")

        # Destructor
        self.bind("<Destroy>", self.on_destroy)

    def __readLogs(self):
        # Do cleanup if another process is already running.
        self.__stopLogs()

        self.log_reader_thread = Thread(target = self.__logWriterThreadFunction, args = [self.stlink_interface, self.log_text_box])
        self.log_reader_thread.daemon = True
        try:
            self.log_reader_thread.start()
            print("Thread started.")
        except Exception as error:
            messagebox.showinfo(title = "Error", message = "Failed to start the log reader's thread. Error:" + str(error))

    # Thread function for writing logs from stdout of STM32CubeProgrammer process to the text box
    # The thread will stop when stdout reaches EOF. It can be triggered by terminating the process using __stopLogs()
    def __logWriterThreadFunction(self, stlink_interface, log_text_box: customtkinter.CTkTextbox):
        stdout = stlink_interface.StartSWVLogReaderProcess()
        log_text_box.configure(state = "normal") # Enable the text box again
        log_text_box.delete("0.0", "end") # Delete all text
        self.log_text_box.insert("end", "-- Starting Log process --\nIf it is failing to connect, make sure that no other program is connected to STM32. Re-plug the STM32 again to the computer and try again\n\n")

        # The readline() will receive an EOF and exit the loop when the STM32Programmer process is terminated
        line = stdout.readline()
        while line:
            log_text_box.insert("end", line)
            line = stdout.readline()

        # FOOTGUN: DO NOT PUT self.log_text_box.insert() beyond here. Otherwise, the thread will not join to the main thread properly!
        # I don't know why but just don't do that!
        print("Process stopped!")

        return

    # Stop the logs if the log process is currently running
    def __stopLogs(self):
        if self.log_reader_thread is None:
            return 
        
        # Stop the STM32CubeProgrammer process
        self.stlink_interface.StopSWVLogReaderProcess()

        self.log_text_box.insert("end", "\n-- Log process has been stopped --\n")

        self.log_text_box.configure(state = "normal")

        # Wait for the low reader thread to join back to the main thread
        self.log_reader_thread.join(timeout = 0.5)
        print(self.log_reader_thread.is_alive)
        self.log_reader_thread = None

    def __saveLogToFile(self):
        # Generate current time as the default text file name
        current_time = datetime.now().strftime("vcu_log_%Y-%d-%m-%H_%M_%S")
        print(current_time)
        
        # Open a file dialog to choose the save location
        file_path = filedialog.asksaveasfilename(initialfile=current_time, 
                defaultextension=".txt", 
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if file_path is None:
            return # No path is selected
            
        try:
            file = open(file_path, 'w')
            log = self.log_text_box.get("1.0", "end-1c")
            file.write(log)
            file.close()
        except Exception as error:
            messagebox.showinfo(title = "Error", message = "Failed to save log to file. Error:" + str(error))
    
    # Destructor to clean up the STM32CubeProgrammer process
    # In case the user closes the program without stopping the logs
    def on_destroy(self, _event):
        print("Destructing Log Viewer Frame...")
        self.__stopLogs()