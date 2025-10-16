from pymodbus.client import ModbusTcpClient
from datetime import datetime, date
import threading
import time
import os, sys
import zipfile

username = os.environ.get("USERNAME")

CONST_POLE = "spo"
CONST_FILETYPE = ".csv"
data_frequency = 60 # The number here defines the frequency of data collection

def make_filename(date: date) -> str:

    username = os.getlogin()
    folder_path = f"C:/Users/{username}/Documents/Icecube"
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    folder_name = f"{str(date.year)[-2:]}_{date.month}"
    folder_path = f"C:/Users/{username}/Documents/Icecube/{folder_name}/"

    #Check if the folder exist, if not, create it

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)



    filename = ""
    filename += CONST_POLE
    filename += str(date.today().year)[-2:]
    filename += "_"
    filename += str(date.timetuple().tm_yday).rjust(3, '0')

    

    filename += CONST_FILETYPE


    return os.path.join(folder_path, filename) 

def record_data(filename: str):
    while not flag.is_set():
        try:
            file_exists = os.path.exists(filename)
            with open(filename, 'a') as f:
                print("Opening file: ", filename)
                print("Recording beginning...")

                if not file_exists:
                    f.write("Date,Time,Device ID,Voltage,Current,Temp,Response\n")

                prev_time = datetime.now()
                prev_time = prev_time.replace(second=(prev_time.second - (prev_time.second % int((60/size)))))
                while not flag.is_set():
                    for i in range(size):
                        print("Recording device %s... (press CTRL+C to save results and quit)" % str(i + 1))
                        while True:
                            if flag.is_set():
                                break
                            current_time = datetime.now()
                            if (current_time - prev_time).total_seconds() >= int(60/size) and current_time != prev_time:
                                prev_time = current_time
                                prev_time = prev_time.replace(second=(prev_time.second - (prev_time.second % int((60/size)))))
                                break
                            response = ser.read_input_registers(address=0x00, count=2, slave=int(unit_arr[i]))
                        try:
                        
                            volt = response.registers[0] / 100
                            curr = response.registers[1] / 100
                            temp = ser.read_input_registers(address=0x00, count=1, slave=1).registers[0] / 10

                            f.write("{},{},{},"
                                    "{},{},{},OK\n".format(datetime.today().date(),
                                                             prev_time.strftime(
                                                                 '%H:%M:%S'),unit_arr[i],
                                                             volt, curr, temp))
                        except AttributeError as e:
                            print("fail")
                            print(e)
                            f.write("{},{},{},"
                                    "{},{},{},NO RESPONSE\n".format(datetime.today().date(),
                                                             prev_time.strftime(
                                                                 '%H:%M:%S'),unit_arr[i],
                                                             "NA", "NA", "NA"))
                        f.flush()
                        time.sleep(1)

                f.close()
                print("File closed")
                    
                                


        except FileNotFoundError as e:
            print("File not found: ", e)
            break
        
        except PermissionError as e:
            print("Permission denied. Please ensure the file is closed before running program.")
            quit()
            break
            
    ser.close()     
    print("Recording ending...")
        



ser = ModbusTcpClient('192.168.28.104', #Most likely needs to be manually entered for automatic running of program
                      port = 8899)
def detect_devices(client, start_id=2, end_id=8, address=0x00, count=1):
    detected_units = []
    for unit_id in range(start_id, end_id + 1):
        try:
            response = client.read_input_registers(address=address, count=count, slave=unit_id)
            if response and hasattr(response, 'registers'):
                # Device responded, add to list
                detected_units.append(str(unit_id))
                print(f"Device {unit_id} detected.")
            else:
                print(f"No response from device {unit_id}.")
        except Exception as e:
            print(f"Error communicating with device {unit_id}: {e}")
    return detected_units

unit_arr = detect_devices(ser, 2, 8)
size = len(unit_arr)

if size == 0:
    print("No devices detected. Exiting.")
    sys.exit()
def zip_month_folder(year: int, month: int):
    username = os.getlogin()
    folder_name = f"{str(year)[-2:]}_{month}"
    folder_path = f"C:/Users/{username}/Documents/Icecube/{folder_name}/"
    zip_filename = os.path.join(folder_path, f"{folder_name}.zip")
    
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist, skipping zipping.")
        return
    
    print(f"Zipping folder {folder_path} into {zip_filename}...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
                    
    print(f"Zipping complete.")

if connect_str := ser.connect():

    print("Connection found" if ser.is_socket_open() else "No connection found")

    current_time = time.time()
    date = datetime.now().date()
    filename = make_filename(date)

    flag = threading.Event()
    recording_thread = threading.Thread(target=record_data, args=(filename,))
    recording_thread.start()


    try:
        while True:
            
            new_date = datetime.now().date()
            if date.month != new_date.month or date.year != new_date.year:
                flag.set()
                time.sleep(2)
    
                # Zip the previous month's folder before resetting
                zip_month_folder(date.year, date.month)
    
                # Reset
                date = new_date
                filename = make_filename(date)
                flag.clear()
                recording_thread = threading.Thread(target=record_data, args=(filename,))
                recording_thread.start()

                
    except KeyboardInterrupt as e:
        flag.set()

    recording_thread.join()
    print("Program exiting...")





