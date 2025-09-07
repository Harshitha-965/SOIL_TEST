import serial

# Replace 'COM3' with your Arduino's COM port (Windows) or '/dev/ttyUSB0' (Linux/Mac)
arduino_port = 'COM7'  
baud_rate = 9600  

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")

    while True:
        line = ser.readline().decode('utf-8').strip()  # Read and decode data
        if line:
            print("Received from Arduino:", line)  # Print the received data

except serial.SerialException as e:
    print(f"Error: {e}")
