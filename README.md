# PZEM Reader (Device 0)

This repository contains a Python-based script to interface with PZEM energy monitoring devices using Modbus TCP. The script automates data recording, handles connection management, and logs data into CSV files.

## Features

- Connects to PZEM devices via Modbus TCP.
- Automatically generates and manages CSV files for daily logs.
- Periodically records voltage, current, and temperature.
- Handles errors such as device disconnection or communication failure.

## Requirements

- Python 3.6+
- Required Python packages:
  - `pymodbus`
  - `datetime`
  - `threading`
  - `os`
  - `sys`
- A PZEM device accessible via Modbus TCP.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the repository:
   ```bash
   cd <repository-folder>
   ```

3. Install dependencies:
   ```bash
   pip install pymodbus
   ``` 

## Configuration

- Update the `ser = ModbusTcpClient` section in the script with your device's IP address and port.
- Modify the `CONST_DEVICE_ID` if you are using a device ID other than `0`.

## Usage

1. Run the script:
   ```bash
   python PZEMReader(Device0).py
   ```

2. The script will automatically:
   - Attempt to connect to the specified PZEM device.
   - Generate a new CSV file for daily logs in the `Documents/Icecube` folder.
   - Record voltage, current, and temperature periodically.

3. To stop the script, press `CTRL+C`. The current session will be saved.

## File Management

- Files are stored in the `Documents/Icecube` directory under a folder named by the current year and month (e.g., `24_12` for December 2024).
- Filenames are structured as follows:
  ```
  <POLE><YY>_<DAY_OF_YEAR>_device_<DEVICE_ID>.csv
  ```
  Example: `spo24_345_device_0.csv`

## Error Handling

- The script handles errors such as:
  - File not found
  - Permission issues
  - Sensor disconnection or communication failure
- Logs `NO RESPONSE` for failed data reads.

## Contact

For further information or questions, please contact:
- Manish Khanal (manish.khanal@utah.edu)
- Hayden Soelberg (hwsoelberg@gmail.com)
