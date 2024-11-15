import serial
import time

# Configuration
PORT = "/dev/ttyACM0"  # Replace with your ESP32-C3's serial port
BAUDRATE = 115200

def send_command(command):
    """
    Sends a command to the ESP32-C3 over Serial.
    """
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            ser.write(f"{command}\n".encode())  # Send command
            time.sleep(0.1)  # Wait briefly for response
            response = ser.read_all().decode().strip()  # Read response
            return response
    except serial.SerialException as e:
        return f"Error: {e}"

def main():
    print("ESP32-C3 GPIO Controller")
    print("Commands: onX, offX (where X is 0-9) or 'exit' to quit")

    while True:
        command = input("Enter command: ").strip()
        if command.lower() == "exit":
            print("Exiting...")
            break

        response = send_command(command)
        if response:
            print("Response:", response)
        else:
            print("No response from ESP32-C3")

if __name__ == "__main__":
    main()
