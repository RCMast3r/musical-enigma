import tkinter as tk
import time
import random
import serial
import time
from pygame import mixer

# Configuration
PORT = "/dev/ttyACM0"  # Replace with your ESP32-C3's serial port
BAUDRATE = 115200

# Define home row keys and their positions on the grid
home_row_keys = ['Q', 'W', 'E', 'R', 'V']
# Reminder of what the note being played is. These notes go 1-1 with the keys
home_row_notes = ['C', 'D', 'E', 'F', 'G']
key_widgets = {}
target_key = None
reaction_time = 50  # max reaction time in ms
# Init Audio
mixer.init()
# Twinkle Twinkle Little Star
song_sequence = [
    'Q', 'Q', 'R', 'R', 'V', 'V', 'R',  # C C G G A A G
    'W', 'W', 'E', 'E', 'W', 'W', 'Q',  # F F E E D D C
    'R', 'R', 'W', 'W', 'E', 'E', 'W',  # G G F F E E D
    'R', 'R', 'W', 'W', 'E', 'E', 'W',  # G G F F E E D
    'Q', 'Q', 'R', 'R', 'V', 'V', 'R',  # C C G G A A G
    'W', 'W', 'E', 'E', 'W', 'W', 'Q'   # F F E E D D C
]

note_durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0,  # "Twinkle Twinkle Little Star"
                  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0,  # "How I wonder what you are"
                  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0,  # "Twinkle Twinkle Little Star"
                  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0,  # "How I wonder what you are"
                  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0,  # "Twinkle Twinkle Little Star"
                  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0]  # "How I wonder what you are"

current_note_index = 0  # Index to track the current note in the sequence


def play_sound(note):
    mixer.music.load(f"notes/{note}.wav")
    mixer.music.play()

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
        play_sound(target_key)
        if elapsed_time <= reaction_time:
            key_widgets[target_key].config(bg="green")
        else:
            key_widgets[target_key].config(bg="red")
        reset_key()
    
    
# Function to reset the target key's color after a short delay
def reset_key():
    global target_key, current_note_index
    if target_key is None:
        return
    # Capture the current target key to ensure it doesn't change during the delay
    current_key = target_key
    key_widgets[current_key].after(reaction_time, lambda: key_widgets[current_key].config(bg="lightgray"))
    target_key = None
    duration = note_durations[current_note_index - 1] * 1000
    root.after(int(duration), display_key)  # Show a new key after a delay

# Function to randomly highlight a key
def display_key():
    global target_key, start_time, current_note_index
    if target_key is None:
        target_key = song_sequence[current_note_index]
        key_widgets[target_key].config(bg="red")
        resp = send_key_command(target_key)
        # print(resp)
        start_time = time.time()  # Record the time when the key is highlighted
        current_note_index = (current_note_index + 1) % len(song_sequence)


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
