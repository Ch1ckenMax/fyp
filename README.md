# Final Year Project

# Current Logic Improvement
- Logging Errors with CAN/SD Card
- Regen Mode: Activation on braking
- Simplifications on APPS logic

# Streamlined Config UI
- Config Change/Upload to flash memory
- Config file on client side to see what kind of parameters can be changed
- Mechanism on the target machine to parse and read the parameters correctly
- Calibration tool: host machine reading data from serial
- `python3 -m ensurepip`
- `python3 -m pip install -r requirements.txt`
- Flashing with cubeide will flash away all memory, but with stlink it wont?
- Don't connect stm32 with more than 1 software

# Dashboard
- Design a CAN Message received by: Dashboard + Data Aquisition Board
- Create UI for the dashboard

# Data Analysis Tool (Nice to have)
- csv -> graph
- show brake/gas/other kinds of data on the graph
- separate each by laptimes (checkbox to show laptimes. csv parsing)
