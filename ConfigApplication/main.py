from src.stlinkinterface import VCUInterface

# Load Config

# Create a GUI

# Check if ST-LINK exists in the env var

vcuInterface = VCUInterface(0, 1)

print(vcuInterface.HasConnection())