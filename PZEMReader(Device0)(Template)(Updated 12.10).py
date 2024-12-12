from pymodbus.client import ModbusTcpClient
from datetime import datetime, date
import pymodbus.exceptions
import threading
import time
import os, sys

CONST_POLE = "spo"
CONST_FILETYPE = ".csv"
CONST_DEVICE_ID = 0

def make_filename(date: date) -> str:

    username = os.getlogin()

    folder_path = f"C:/Users/{username}/Documents/Icecube"

    if not os.path.exists(folder_path):
        
        os.mkdir(folder_path)


    folder_name = f"{str(date.year)[-2:]}_{date.month}"

    folder_path = f"C:/Users/{username}/Documents/Icecube/{folder_name}/"
    
    # Check if the folder exists, if not, create it

    if not os.path.exists(folder_path):

        os.mkdir(folder_path)


    filename = ""
    filename += CONST_POLE
    filename += str(date.today().year)[-2:]
    filename += "_"
    filename += str(date.timetuple().tm_yday).rjust(3, '0')
    filename += "_"
    filename += f"device_{CONST_DEVICE_ID}"
    filename += ""

    

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
                    print("Recording device %s... (press CTRL+C to save results and quit)" % str(CONST_DEVICE_ID))
                    while True:
                        if flag.is_set():
                            break
                        current_time = datetime.now()
                        if (current_time - prev_time).total_seconds() >= int(60/size) and current_time != prev_time:
                            prev_time = current_time
                            prev_time = prev_time.replace(second=(prev_time.second - (prev_time.second % int((60/size)))))
                            break
                    
                    try:
                        
                        registers = ser.read_input_registers(0x00,2,
                                                         slave = unit_id)
                    
                        volt = registers.registers[0] / 100
                        curr = registers.registers[1] / 100
                        temp = ser.read_input_registers(0x00,1,
                                                         slave = 1).registers[0] / 10

                        f.write("{},{},{},"
                                "{},{},{},OK\n".format(datetime.today().date(),
                                                         prev_time.strftime(
                                                             '%H:%M:%S'),
                                                       unit_id,
                                                         volt, curr, temp))
                    except AttributeError as e:
                        print("fail to read sensors")
                        print(e)
                        f.write("{},{},{},"
                                "{},{},{},NO RESPONSE\n".format(datetime.today().date(),
                                                         prev_time.strftime(
                                                             '%H:%M:%S'),
                                                        unit_id,
                                                         "NA", "NA", "NA"))

                    except pymodbus.exceptions.ConnectionException as e:
                        print("failed to connect to sensors")
                        print(e)
                        f.write("{},{},{},"
                                "{},{},{},NO RESPONSE\n".format(datetime.today().date(),
                                                         prev_time.strftime(
                                                             '%H:%M:%S'),
                                                        unit_id,
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

unit_id = CONST_DEVICE_ID
size = 1

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
            if date != datetime.now().date():
                flag.set()
                time.sleep(2)

                #Reset
                date = datetime.now().date()
                filename = make_filename(date)
                flag.clear()
                recording_thread = threading.Thread(target=record_data, args=(filename,))
                recording_thread.start()
                
    except KeyboardInterrupt as e:
        flag.set()

    recording_thread.join()
    print("Program exiting...")

    sys.exit()
    
else:
    print("No connection found. Program exiting...")

    sys.exit()




    
