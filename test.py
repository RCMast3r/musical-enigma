import tkinter as tk
import time
import random
import serial
import time

# Configuration
PORT = "/dev/ttyACM0"  # Replace with your ESP32-C3's serial port
BAUDRATE = 115200

# Define home row keys and their positions on the grid
home_row_keys = ['Q', 'W', 'E', 'R', 'V']
key_widgets = {}
target_key = None
reaction_time = 50  # max reaction time in ms 

def send_key_command(target_key):
    """
    Sends a command to the ESP32-C3 over Serial.
    """
    try:
        command = "on"+f"{home_row_keys.index(target_key)}"
        print(command)
        # command = "on6"
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            ser.write(f"{command}\n".encode())  # Send command
            time.sleep(0.15)  # Wait briefly for response
            response = ser.read_all().decode().strip()  # Read response
            command = "off"+f"{home_row_keys.index(target_key)}"
            # command = "off6"
            ser.write(f"{command}\n".encode())  # Send command
            response = ser.read_all().decode().strip()  # Read response
            return response
    except serial.SerialException as e:
        return f"Error: {e}"
    
# Function to start checking the user's key press
def check_key_press(event):
    global target_key
    if target_key is None:
        return
    
    # print("key target: ",target_key)
    if event.keysym.upper() == target_key or ((target_key==';') and (event.keysym.upper()=='SEMICOLON')):
        elapsed_time = (time.time() - start_time) * reaction_time  # in ms
        if elapsed_time <= reaction_time:
            key_widgets[target_key].config(bg="green")
        else:
            key_widgets[target_key].config(bg="red")
        reset_key()
    
    
# Function to reset the target key's color after a short delay
def reset_key():
    global target_key
    if target_key is None:
        return
    # Capture the current target key to ensure it doesn't change during the delay
    current_key = target_key
    key_widgets[current_key].after(reaction_time, lambda: key_widgets[current_key].config(bg="lightgray"))
    target_key = None
    root.after(reaction_time, display_key)  # Show a new key after a delay

# Function to randomly highlight a key
def display_key():
    global target_key, start_time
    if target_key is None:
        target_key = random.choice(home_row_keys)
        key_widgets[target_key].config(bg="red")
        resp = send_key_command(target_key)
        # print(resp)
        start_time = time.time()  # Record the time when the key is highlighted

# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Home Row Typing Trainer")

# Create key buttons
for idx, key in enumerate(home_row_keys):

    key_widgets[key] = tk.Label(root, text=key, width=4, height=2, bg="lightgray", font=("Helvetica", 18), relief="raised")
    key_widgets[key].grid(row=0, column=idx, padx=5, pady=10)

# Bind the key press event
root.bind("<KeyPress>", check_key_press)

# Start displaying keys in a separate thread
root.after(1000, display_key)  # Start displaying keys after a short delay
root.mainloop()
