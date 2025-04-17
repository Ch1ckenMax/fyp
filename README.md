# Final Year Project

# Streamlined Config UI
- Config Change/Upload to flash memory
- Config file on client side to see what kind of parameters can be changed
- Mechanism on the target machine to parse and read the parameters correctly
- Calibration tool: host machine reading data from serial
- `python3 -m ensurepip`
- `python3 -m pip install -r requirements.txt`
- Flashing with cubeide will flash away all memory, but with stlink it wont?
- Don't connect stm32 with more than 1 software
- STM32CubeCLT1.16.0
- https://www.codeproject.com/Articles/16163/Real-Time-Console-Output-Redirection
- https://stackoverflow.com/questions/50315088/how-to-limit-the-buffer-size-of-a-pipe-windows

# Simulated Test with Arduino
- Mimick the MCU in the vehicle
- Flooding the CAN bus with different message id to emulate heavy traffic/ heavy packet loss from electromagnetic interference
